<br/>

<p align="center">
  <img src="../design/graphics/svg/xcore_full_green.svg" width=350px alt="">
    <br/><br/>
    <b>a simple modular application that provides various functionalities in the form of modules</b>
</p>

<p align="center">
    <a href="../LICENSE"><img src="https://img.shields.io/badge/Code-MIT-yellow.svg" alt=""></a>
    <a href=""><img src="https://img.shields.io/badge/powered%20by-Xeniorn-4770DB" alt=""></a>
    <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/Media-CC%20BY%204.0-lightgrey.svg" alt=""></a>
    <a href="https://github.com/x404bjrn"><img src="https://img.shields.io/badge/written%20by-x404bjrn-8A2BE2" alt=""></a>
</p>

---

[![DE](https://img.shields.io/badge/DE-blue?style=for-the-badge)](../README.md)
![EN](https://img.shields.io/badge/EN-green?style=for-the-badge)

## Overview

The XCORE Framework is a modular, extensible Python framework that enables centralized control, execution, and development of automation tools, security modules, creative helper scripts, and low-level system applications through CLI, GUI, or web interface.

### ✨ Highlights

#### 🔌 Plug-and-Play Modules
- Load, configure, and execute modules using a Metasploit-like workflow (use, options, run) – locally or remotely.

#### 🧠 User-Friendly & Multilingual
- Dynamic GUI with automatic widget generation for module options, integrated translation support (i18n), and user management.

#### 🌐 Three Control Interfaces
- CLI for power users
- Tkinter-based GUI for the desktop
- Web interface (Flask + React) for remote access and a modern UI

#### 💾 Database-Backed Module Options
- Save custom settings, reload them later, or distribute them centrally.

#### ⚒️ Integrated Dev Tools
- Built-in tools like the module creator, Setpoint editor, auto-localization, and ENV setup make development and deployment efficient and consistent.

#### For comprehensive documentation, see [DOCUMENTATION_EN.md](../docs/DOCUMENTATION_EN.md).

---

## Key Features

**Modular Structure**: The framework organizes functionalities into various module categories like Scanner, AI, Utilities, OSINT, System, Monitor, Exploitation, Helper, Persistence, Creative, and Transfer.

**Multiple Operating Modes**:
- **CLI Mode**: An interactive command line for executing modules
- **GUI Mode**: A graphical user interface for ease of use
- **Web Mode**: A web interface for remote access
- **Setpoint Mode**: A configuration editor with CLI, GUI, or web interface

**Multilingualism**: Support for multiple languages (currently German and English) with a flexible internationalization structure.

**Extensibility**: New modules can be added easily to extend functionality.

---

## Installation

### Requirements

- Python 3.8 or higher
- pip (Python package manager)

### Installation via pip
```bash
pip install xcore_framework
```
### Installation from Source Code

1. Clone the repository:
```bash
git clone https://github.com/x404bjrn/XCORE.git
```

2. Change to the directory:
```bash
cd XCORE
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Perform the installation:
```bash
pip install -e .
```
or
```bash
python setup.py install
```

---

## 🚀 Quick Start

### Start CLI Mode
```
bash
xcore --cli
```
### Start Web Mode
```
bash
xcore --web
```
Optional parameters:
- `--host`: Host address (default: 127.0.0.1)
- `--port`: Port (default: 5000)
- `--debug`: Enable debug mode
- `--open-browser`: Automatically open browser (default: enabled)

Example:
```
bash
xcore --web --host 0.0.0.0 --port 8080 --debug
```
### Start GUI Mode
```
bash
xcore --gui
```
### Start Setpoint Mode
```
bash
xcore --setpoint
```
Optional parameters:
- `--interface`: Interface for the configuration editor (cli, gui, web) (default: gui)

Example:
```
bash
xcore --setpoint --interface cli
```
---

## Creating Custom Modules

The XCORE Framework includes a graphical tool for creating modules, located under `dev/tools/module_creator.py`. This tool simplifies the process of creating new modules by providing a user-friendly interface for defining module metadata, options, and internationalization strings.

For detailed information on creating custom modules, see the [Module System](../docs/DOCUMENTATION_EN.md#module-system) section in the documentation.

---

## Contributing

Contributions to the XCORE Framework are welcome! Here are some ways you can contribute:

1. **Report a bug**: Create an issue in the GitHub repository if you find a bug.
2. **Suggest features**: Have an idea for a new feature? Create an issue with your suggestion.
3. **Contribute code**: Fork the repository, make your changes, and create a pull request.
4. **Create modules**: Create new modules to extend the framework's functionality.

---

## License

- **Code**: MIT License – see [LICENSE](../LICENSE) for details
- **Media Content**: CC BY 4.0 – see [Creative Commons](https://creativecommons.org/licenses/by/4.0/) for details

---

## written on the dark side of toast 🍞🌚  
#### © 2025, [Xeniorn](https://xeniorn.de) | [`x404bjrn`](https://github.com/x404bjrn)