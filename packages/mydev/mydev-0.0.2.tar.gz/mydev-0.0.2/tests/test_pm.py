import os
import tempfile
from time import sleep

from mydev.db import init_db
from mydev.pm.manager import run_and_redirect, Manager


def test_run_and_redirect():
    cmd = "python -c 'for idx in range(5): print(idx)'"
    with tempfile.TemporaryDirectory() as temp_dir:
        redir_path = f"{temp_dir}/output.txt"
        run_and_redirect(cmd, redir_path)
        with open(redir_path) as f:
            assert f.read() == "0\n1\n2\n3\n4\n"

    cmd = "bash -c 'for idx in {0..4}; do echo $idx; done'"
    with tempfile.TemporaryDirectory() as temp_dir:
        redir_path = f"{temp_dir}/output.txt"
        run_and_redirect(cmd, redir_path)
        with open(redir_path) as f:
            assert f.read() == "0\n1\n2\n3\n4\n"

    py_script = """
from rich.progress import track
for idx in track(range(5)):
    print(idx)
    """.strip()
    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = f"{temp_dir}/script.py"
        with open(script_path, "w") as f:
            f.write(py_script)
        cmd = f"python {os.path.abspath(script_path)}"
        redir_path = f"{temp_dir}/output.txt"
        run_and_redirect(cmd, redir_path)
        with open(redir_path) as f:
            assert f.read() == "0\n1\n2\n3\n4\nWorking... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00\n"

    py_script = "import non_existent_module"
    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = f"{temp_dir}/script.py"
        with open(script_path, "w") as f:
            f.write(py_script)
        cmd = f"python {os.path.abspath(script_path)}"
        redir_path = f"{temp_dir}/output.txt"
        ret_code = run_and_redirect(cmd, redir_path)
        assert ret_code != 0
        with open(redir_path) as f:
            assert "ModuleNotFoundError" in f.read()


def test_manager():
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_db_url = f"sqlite:///{temp_dir}/db.sqlite"
        mock_pm_dir = f"{temp_dir}/pm"
        init_db(mock_db_url)
        manager = Manager(pm_dir=mock_pm_dir, db_url=mock_db_url)
        cmd = "python -c 'print(\"Hello\")'"
        manager.run(cmd)
        sleep(0.1)
        proc = manager.list_proc()[0]
        assert "Hello" in proc.cmd
        assert proc.status == "completed"
        assert os.path.exists(f"{mock_pm_dir}/{proc.id}/stdout")
        out = manager.cat(proc.id)
        assert "Hello" in out

    with tempfile.TemporaryDirectory() as temp_dir:
        mock_db_url = f"sqlite:///{temp_dir}/db.sqlite"
        mock_pm_dir = f"{temp_dir}/pm"
        init_db(mock_db_url)
        manager = Manager(pm_dir=mock_pm_dir, db_url=mock_db_url)
        cmd = 'python -c \'while True: print("Hello"); __import__("time").sleep(0.01)\''
        manager.run(cmd)
        sleep(0.1)
        proc = manager.list_proc()[0]
        assert "Hello" in proc.cmd
        assert proc.status == "running"

        out = manager.cat(proc.id)
        prev_len = len(out)
        assert "Hello" in out

        sleep(0.1)
        out = manager.cat(proc.id)
        assert len(out) > prev_len

        manager.kill(proc.id)
        sleep(0.1)
        proc = manager.list_proc()[0]
        assert proc.status == "failed"
