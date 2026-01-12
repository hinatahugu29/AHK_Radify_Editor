# Installation

This page explains how to install Radify Menu Editor.

## System Requirements

### Required Environment

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 or higher
- **AutoHotkey**: v2.0 or higher (for running generated scripts)

!!! note "Python Version"
    Python 3.8 or higher is required. Check with `python --version` command.

## Installation Steps

### 1. Install Python

If Python is not installed, download and install it from the [official website](https://www.python.org/downloads/).

!!! warning "Important"
    Make sure to check "Add Python to PATH" during installation.

### 2. Install AutoHotkey v2

AutoHotkey v2 can be downloaded from the [official website](https://www.autohotkey.com/).

!!! info "Difference from AutoHotkey v1"
    This editor is **v2 only**. It will not work with v1.

### 3. Download the Project

Clone or download the project from the GitHub repository.

#### Using Git

```bash
git clone https://github.com/hinatahugu29/AHK_Radify_Editor.git
cd AHK_Radify_Editor
```

#### Download as ZIP

1. Access the [GitHub repository](https://github.com/hinatahugu29/AHK_Radify_Editor)
2. Click "Code" → "Download ZIP"
3. Extract the downloaded ZIP file

### 4. Install Python Packages

Run the following command in the project folder:

```bash
pip install -r requirements.txt
```

Packages to be installed:

- **CustomTkinter**: Modern GUI framework
- **Pillow**: Image processing library

## How to Launch

Once installation is complete, launch the editor with:

```bash
python main.py
```

!!! success "Launch Successful"
    If a window appears, installation was successful!

## Troubleshooting

### Python Not Recognized

If the `python` command is not recognized, try:

1. Try the `python3` command
2. Add Python to the PATH environment variable
3. Reinstall Python (check "Add to PATH")

### Package Installation Error

Try running with administrator privileges:

```bash
pip install --user -r requirements.txt
```

### Module Not Found Error

Verify that all required files are present:

- `main.py`
- `modules/` folder
- `requirements.txt`

## Next Steps

Once installation is complete, create your first menu with the [Quick Start Guide](quickstart.md)!
