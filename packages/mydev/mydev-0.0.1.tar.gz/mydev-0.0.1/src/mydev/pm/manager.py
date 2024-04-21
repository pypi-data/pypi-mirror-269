import os
import shlex
import shutil
import subprocess
import sys
from threading import Thread
from typing import Callable
import psutil

from sqlmodel import Session, select, create_engine

from mydev.pm.models import Process, Status
from mydev.utils.constants import MYDEV_PM_DIR, MYDEV_DB_URL


# TODO: make it async
def run_and_redirect(command: str, redir_path: str, callbacks: tuple[Callable] = ()) -> int:
    def redirect_to_file(_stream, _file_path):
        with open(_file_path, "w") as f:
            while True:
                text = _stream.readline().decode("utf-8")
                if not text:
                    break
                f.write(text)
                f.flush()

    os.environ["PYTHONUNBUFFERED"] = "1"
    os.environ["PATH"] = os.environ["PATH"] + f":{os.path.dirname(sys.executable)}"  # add current python path to PATH

    popen = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for callback in callbacks:
        callback(popen)

    thread = Thread(target=redirect_to_file, args=(popen.stdout, redir_path), daemon=True)
    thread.start()

    popen.wait()
    thread.join()

    return popen.returncode


class Manager:
    def __init__(self, pm_dir: str = MYDEV_PM_DIR, db_url: str = MYDEV_DB_URL):
        self.pm_dir = pm_dir
        self.engine = create_engine(db_url)
        os.makedirs(self.pm_dir, exist_ok=True)

    def run(self, cmd: str, alias: str | None = None):
        with Session(self.engine) as session:
            proc = Process(cmd=cmd, alias=alias)
            session.add(proc)
            session.commit()
            session.refresh(proc)

            # fork a process
        pid = os.fork()

        if pid == 0:  # the forked child process
            with Session(self.engine) as session:
                proc = session.get(Process, proc.id)

                def pid_callback(_popen):
                    proc.pid = _popen.pid
                    proc.status = Status.running
                    session.add(proc)
                    session.commit()
                    session.refresh(proc)

                stdout_path = os.path.join(self.pm_dir, str(proc.id), "stdout")
                os.makedirs(os.path.dirname(stdout_path), exist_ok=True)

                ret_code = run_and_redirect(cmd, stdout_path, callbacks=(pid_callback,))

                session.refresh(proc)
                if ret_code == 0:
                    proc.status = Status.completed
                else:
                    proc.status = Status.failed
                session.add(proc)
                session.commit()

            # exit the child process
            os._exit(0)  # noqa

    def list_proc(self) -> list[Process]:
        with Session(self.engine, expire_on_commit=False) as session:
            statement = select(Process)
            processes = session.exec(statement)
            processes: list[Process] = list(processes)
        return processes

    def remove(self, proc_id: int) -> bool:
        with Session(self.engine) as session:
            statement = select(Process).where(Process.id == proc_id)
            proc = session.exec(statement).first()
            if not proc:
                return False
            session.delete(proc)
            session.commit()
        shutil.rmtree(os.path.join(self.pm_dir, str(proc_id)), ignore_errors=True)
        return True

    def kill(self, proc_id) -> bool:
        with Session(self.engine) as session:
            statement = select(Process).where(Process.id == proc_id)
            proc = session.exec(statement).first()
            if not proc:
                return False
            parent = psutil.Process(proc.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
            proc.status = Status.failed
            session.add(proc)
            session.commit()
        return True

    def cat(self, proc_id) -> str:
        with open(os.path.join(self.pm_dir, str(proc_id), "stdout")) as f:
            return f.read()
