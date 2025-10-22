#!/usr/bin/env zsh
set -euo pipefail

# Usage:
# ./setup_spacy_tm_py311.sh [--python /path/to/python3.11] [--dir /path/to/project] [--model en_core_web_sm]
#
# Examples:
# ./setup_spacy_tm_py311.sh
# ./setup_spacy_tm_py311.sh --model en_core_web_sm
# ./setup_spacy_tm_py311.sh --python /opt/homebrew/bin/python3.11 --dir /Users/ceciliabarnard/Desktop/8510/TopicModeling --model en_core_web_trf

PYTHON_BIN_DEFAULT="/opt/homebrew/bin/python3.11"
VENV_NAME="tm_py311"
SPACY_VERSION="3.7.5"
PROJECT_DIR_DEFAULT="$(pwd)"   # default: run from the desired folder (TopicModeling)

# parse args
PYTHON_BIN="$PYTHON_BIN_DEFAULT"
PROJECT_DIR="$PROJECT_DIR_DEFAULT"
MODEL_TO_INSTALL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --python)
      shift; PYTHON_BIN="$1"; shift;;
    --dir)
      shift; PROJECT_DIR="$1"; shift;;
    --model)
      shift; MODEL_TO_INSTALL="$1"; shift;;
    -h|--help)
      echo "Usage: $0 [--python /path/to/python3.11] [--dir /path/to/project] [--model en_core_web_sm]"
      exit 0;;
    *)
      echo "Unknown arg: $1"; exit 2;;
  esac
done

echo "Project dir: $PROJECT_DIR"
echo "Python binary: $PYTHON_BIN"
echo "Venv name: $VENV_NAME"
echo "spaCy version: $SPACY_VERSION"
if [[ -n "$MODEL_TO_INSTALL" ]]; then
  echo "Will also install spaCy model: $MODEL_TO_INSTALL"
fi

# ensure project directory exists
if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Error: project dir not found: $PROJECT_DIR" >&2
  exit 1
fi

cd "$PROJECT_DIR"

# find a python binary
if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Warning: $PYTHON_BIN not executable, trying to locate python3.11 or python3..."
  if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3.11)"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
  else
    echo "No suitable python binary found. Install python3.11 (Homebrew: brew install python@3.11) or pass --python." >&2
    exit 1
  fi
fi

echo "Using python: $PYTHON_BIN"

# create venv
if [[ -d "$VENV_NAME" ]]; then
  echo "Venv '$VENV_NAME' already exists; skipping creation."
else
  echo "Creating virtualenv $VENV_NAME..."
  "$PYTHON_BIN" -m venv "$VENV_NAME"
fi

# activate venv in the script
# shellcheck disable=SC1091
source "$VENV_NAME/bin/activate"

# upgrade packaging tools
echo "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

# install spaCy pinned version
echo "Installing spaCy==$SPACY_VERSION..."
pip install "spacy==${SPACY_VERSION}"

# verify installation
echo "Verifying installation..."
python -c "import sys, spacy; print('python', sys.version.split()[0], 'spacy', spacy.__version__)"

# optionally install a spaCy model
if [[ -n "$MODEL_TO_INSTALL" ]]; then
  echo "Installing spaCy model: $MODEL_TO_INSTALL ..."
  # prefer python -m spacy download if available; fall back to pip install if user provided a pip package name
  if python - <<PY >/dev/null 2>&1
import importlib.util, sys
spec = importlib.util.find_spec("spacy.cli")
print(spec is not None)
PY
  then
    python -m spacy download "$MODEL_TO_INSTALL"
  else
    pip install "$MODEL_TO_INSTALL" || {
      echo "Model install via pip failed; try 'python -m spacy download $MODEL_TO_INSTALL' manually." >&2
    }
  fi
fi

# run spacy validate for sanity check
echo "Running 'python -m spacy validate'..."
python -m spacy validate || true

echo "Done. To use this venv in a shell run:"
echo "  cd \"$PROJECT_DIR\""
echo "  source $VENV_NAME/bin/activate"
echo "Then run 'python' or your scripts as usual."