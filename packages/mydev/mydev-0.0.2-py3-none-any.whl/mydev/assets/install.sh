# platforms: linux, darwin, win (git bash)
detect_platform() {
  platform=$(uname -s | tr '[:upper:]' '[:lower:]')
  case $platform in
    linux*) platform="linux" ;;
    darwin*) platform="mac" ;;
    mingw*|msys*|cygwin*) platform="win" ;;
    *) platform="unknown" ;;
  esac
  echo $platform
}

check_and_install_conda() {
  if ! command -v curl &> /dev/null; then
    echo "curl is not installed, please install curl first"
    exit 1
  fi

  if command -v conda &> /dev/null || [ -e "$HOME"/miniconda3 ]; then
    echo "Conda is already installed"
  else
    echo "Conda is not installed, installing..."
    case $PLATFORM in
      linux)
        mkdir -p "$HOME"/miniconda3
        curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o "$HOME"/miniconda3/miniconda.sh
        bash "$HOME"/miniconda3/miniconda.sh -b -u -p "$HOME"/miniconda3
        rm -rf "$HOME"/miniconda3/miniconda.sh
        ;;
      mac)
        mkdir -p "$HOME"/miniconda3
        curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o "$HOME"/miniconda3/miniconda.sh
        bash "$HOME"/miniconda3/miniconda.sh -b -u -p "$HOME"/miniconda3
        rm -rf "$HOME"/miniconda3/miniconda.sh
        ;;
      win)
        curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o miniconda.exe
        start /wait "" miniconda.exe /S
        del miniconda.exe
        ;;
      *)
        echo "Platform not supported"
        exit 1
        ;;
    esac
    echo "Conda installed successfully"
  fi
  source "$HOME"/miniconda3/etc/profile.d/conda.sh
}


check_and_install_mydev() {
  if command -v dev &> /dev/null; then
    echo "mydev is already installed"
    return
  else
    conda activate base
    pip install -q mydev
    echo "mydev installed successfully"
  fi
}

PLATFORM=$(detect_platform)
check_and_install_conda
check_and_install_mydev