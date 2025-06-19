<br/>
<p align="center">
  <img src="https://raw.githubusercontent.com/x404bjrn/XCORE/8c500187b66eb3122b3b0193a8e903b6f270c766/design/graphics/svg/xcore_full_green.svg" width=350px alt="">
    <br/><br/>
    <b>a flexible framework for developing and executing modular functions – usable via console (CLI), graphical user interface (GUI) or web interface</b>
</p>

<p align="center">
    <a href="../LICENSE"><img src="https://img.shields.io/badge/Code-MIT-yellow.svg" alt=""></a>
    <a href="https://pypi.org/project/xcore_framework/"><img src="https://img.shields.io/pypi/v/xcore_framework.svg" alt=""></a>
    <a href=""><img src="https://img.shields.io/badge/powered%20by-Xeniorn-4770DB" alt=""></a>
    <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/Media-CC%20BY%204.0-lightgrey.svg" alt=""></a>
    <a href="https://github.com/x404bjrn"><img src="https://img.shields.io/badge/written%20by-x404bjrn-8A2BE2" alt=""></a>
</p>

---

# Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Operating Modes](#operating-modes)
   - [CLI Mode](#cli-mode)
   - [GUI Mode](#gui-mode)
   - [Web Mode](#web-mode)
   - [Setpoint Mode](#setpoint-mode)
6. [Module System](#module-system)
   - [Module Structure](#module-structure)
   - [Module Categories](#module-categories)
   - [Creating Custom Modules](#creating-custom-modules)
   - [Using the Module Creator](#using-the-module-creator)
7. [Internationalization](#internationalization)
8. [Configuration](#configuration)
9. [Development](#development)
10. [Vision](#vision)
11. [Contributing](#contributing)
12. [License](#license)

---

## Introduction

The XCORE Framework is a versatile, modular application designed to provide a flexible platform for various tasks through a system of pluggable modules. It offers multiple interfaces (CLI, GUI, Web) to accommodate different user preferences and use cases, making it adaptable to various environments and requirements.

This documentation provides comprehensive information about the XCORE Framework, its architecture, functionality, and how to extend it with custom modules.

## Project Overview

### Purpose

The XCORE Framework was created to provide a unified platform where various functionalities can be implemented as modules and accessed through different interfaces. This approach allows for:

- **Flexibility**: Users can choose the interface that best suits their needs
- **Extensibility**: New functionalities can be added without modifying the core framework
- **Modularity**: Components are isolated, making the system easier to maintain and extend
- **Consistency**: Common functionality is shared across interfaces

### Key Features

- **Modular Architecture**: Functionality is organized into modules that can be loaded and executed on demand
- **Multiple Interfaces**: 
  - Command Line Interface (CLI) for terminal-based operation
  - Graphical User Interface (GUI) for desktop users
  - Web Interface for remote access
  - Setpoint Mode for configuration management
- **Internationalization**: Support for multiple languages (currently German and English)
- **User Management**: Authentication and user-specific settings
- **Configuration Management**: Centralized configuration through environment variables
- **Module Creator Tool**: Graphical tool for creating new modules

## Installation

### Prerequisites

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

### Building the Package

If you want to build the package and install it from the wheel file:

1. Install the build package:
   ```bash
   pip install build
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Install the wheel file:
   ```bash
   pip install dist/*.whl
   ```

## Project Structure

The XCORE Framework is organized into several key directories:

```
xcore_framework/
├── config/             # Configuration files
│   ├── i18n/           # Internationalization files
│   └── ...
├── core/               # Core functionality
│   ├── commander.py    # CLI implementation
│   ├── module_loader.py # Module loading system
│   ├── module_base.py  # Base class for modules
│   └── ...
├── database/           # Database functionality
├── gui/                # Graphical User Interface
│   ├── gui.py          # Main GUI implementation
│   └── ...
├── modules/            # Module directories
│   ├── ai/             # AI modules
│   ├── creative/       # Creative modules
│   ├── ...
│   └── template/       # Module templates
├── setpoint/           # Configuration editor
│   ├── setpoint_cli.py # CLI interface for setpoint
│   ├── setpoint_gui.py # GUI interface for setpoint
│   ├── setpoint_web.py # Web interface for setpoint
│   └── ...
├── web/                # Web interface
│   ├── app/            # Flask application
│   └── ...
├── .env                # Environment variables
└── main.py             # Main entry point
```

Additionally, the development tools and frontend code are located in:

```
dev/
├── tools/
│   ├── module_creator.py # Tool for creating modules
│   └── ...
└── frontend/
    └── web/              # Web frontend (React)
        ├── src/          # Source code
        └── ...
```

## Operating Modes

The XCORE Framework offers four main operating modes, each providing a different interface for interacting with the framework's functionality.

### CLI Mode

The Command Line Interface (CLI) mode provides a text-based interface for interacting with the XCORE Framework. It's ideal for server environments, automation scripts, or users who prefer terminal-based workflows.

#### Starting CLI Mode

```bash
xcore --cli
```

#### Key Features

- Interactive command shell with tab completion
- Commands for module management (search, use, list, info)
- Parameter configuration (set, show options)
- Module execution (run)
- User management (login, logout, create, delete)
- Configuration management (save_options, load_options)
- Language settings (lang)

#### Common Commands

- `search <keyword>`: Search for modules containing the keyword
- `use <module_path>`: Load a module for use
- `list`: List all available modules
- `info`: Show information about the current module
- `show options`: Display configurable parameters for the current module
- `set <parameter> <value>`: Set a parameter value
- `run`: Execute the current module with the configured parameters
- `back`: Exit the current module
- `exit`: Exit the CLI

### GUI Mode

The Graphical User Interface (GUI) mode provides a desktop application interface for the XCORE Framework. It's designed for users who prefer a visual interface with forms, buttons, and graphical elements.

#### Starting GUI Mode

```bash
xcore --gui
```

#### Key Features

- User-friendly desktop application
- Visual module selection and configuration
- Form-based parameter input
- Real-time feedback during module execution
- User authentication through login forms
- Consistent styling and layout

#### Interface Components

- Navigation sidebar for module categories
- Module selection interface
- Parameter configuration forms
- Console output display
- User authentication forms

### Web Mode

The Web Interface mode provides a browser-based interface for the XCORE Framework. It allows remote access to the framework's functionality and is ideal for distributed teams or accessing the framework from different devices.

#### Starting Web Mode

```bash
xcore --web
```

Optional parameters:
- `--host`: Host address (default: 127.0.0.1)
- `--port`: Port (default: 5000)
- `--debug`: Enable debug mode
- `--open-browser`: Automatically open browser (default: enabled)

Example:
```bash
xcore --web --host 0.0.0.0 --port 8080 --debug
```

#### Key Features

- Modern, responsive web interface
- RESTful API for module management and execution
- Category-based module navigation
- Dynamic form generation for module parameters
- Real-time feedback during module execution
- User authentication and session management

#### Web Frontend Architecture

The web frontend is built using modern web technologies:
- React for the user interface
- Axios for API communication
- Component-based architecture for maintainability

Key components:
- Dashboard: Main layout component
- XcoreModules: Module management component
- CategorySelector: For selecting module categories
- ModuleSelector: For selecting specific modules
- ModuleDetails: For configuring module parameters
- ResultDisplay: For showing execution results

#### Web Backend Architecture

The web backend is built using Flask:
- RESTful API endpoints for module management
- Integration with the core module system
- User authentication and session management
- Static file serving for the frontend

Key endpoints:
- `/api/modules`: List all available modules
- `/api/module/<module_path>/meta`: Get metadata for a specific module
- `/api/module/<module_path>/run`: Execute a module with parameters

### Setpoint Mode

The Setpoint Mode provides a configuration editor for the XCORE Framework. It allows users to modify environment variables that control the framework's behavior.

#### Starting Setpoint Mode

```bash
xcore --setpoint
```

Optional parameters:
- `--interface`: Interface for the configuration editor (cli, gui, web) (default: gui)

Example:
```bash
xcore --setpoint --interface cli
```

#### Key Features

- Edit environment variables that control the framework
- Multiple interface options (CLI, GUI, Web)
- Validation of configuration values
- Immediate application of configuration changes

#### Configuration Variables

The Setpoint Mode allows editing of various environment variables, including:
- `XCORE_FRAMEWORK`: Path to the framework directory
- `XCORE_ENV`: Path to the .env file
- `XCORE_CONFIG`: Path to the configuration directory
- `XCORE_I18N`: Path to the internationalization directory
- `XCORE_CORE`: Path to the core directory
- `XCORE_MODULES`: Path to the modules directory
- `XCORE_DATABASE`: Path to the database directory
- `XCORE_WEB_INTERFACE_DIR`: Path to the web interface directory
- `XCORE_WEB_INTERFACE_URL`: URL for the web interface
- `XCORE_LANGUAGE`: Default language for the framework

## Module System

The XCORE Framework's functionality is organized into modules, which are self-contained units that implement specific features. The module system is designed to be extensible, allowing users to create and add their own modules.

### Module Structure

Each module in the XCORE Framework follows a standard structure:

- **Module Class**: A Python class that inherits from `XCoreModule`
- **Metadata**: Information about the module (name, description, author, version, etc.)
- **Options**: Configurable parameters for the module
- **Run Method**: The main execution logic of the module
- **Feedback Method**: For providing output during execution

### Module Categories

Modules are organized into categories based on their functionality:

- **ai**: Modules for artificial intelligence and machine learning
- **creative**: Modules for creative applications
- **exploitation**: Modules for security testing and exploitation
- **helper**: Helper modules for various tasks
- **monitor**: Modules for monitoring systems and networks
- **osint**: Modules for open source intelligence
- **persistence**: Modules for data persistence
- **scanner**: Modules for scanning networks and systems
- **system**: Modules for system operations
- **template**: Templates for creating new modules
- **transfer**: Modules for data transfer
- **utilities**: General utilities

### Creating Custom Modules

To create a custom module for the XCORE Framework, you can use the template in `xcore_framework/modules/template/modul.py` as a starting point. Each module must contain a `Module` class that inherits from `XCoreModule` and implements the required methods.

#### Basic Module Structure

```python
from xcore_framework.config.i18n import i18n
from xcore_framework.core.module_base import XCoreModule

class Module(XCoreModule):
    def __init__(self):
        super().__init__()

    name = i18n.t("module_name.modul_name")
    description = i18n.t("module_name.modul_desc")
    author = "Your Name"
    version = "1.0.0"
    created = "01.01.2025"
    options = {
        "option1": {
            "widget_type": "entry",
            "required": True,
            "default": "default_value",
            "desc": i18n.t("module_name.option_option1_desc")
        }
    }

    def run(self, params: dict, mode="cli", gui_console=None) -> dict | None:
        self.mode = mode
        self.console_widget = gui_console
        self.feedback([i18n.t("module_name.modul_headline")])

        try:
            for key in self.options:
                val = params.get(key, self.options[key].get("default"))
                self.feedback([f"{key}: {val}"])

            # Main module logic here

            self.feedback([i18n.t("module_name.modul_done_message")])
            return {"success": True, "output": self.output, "data": self.results}

        except Exception as e:
            msg = i18n.t("module_name.modul_error", error=e)
            self.feedback([msg])
            return {"success": False, "error": msg, "output": [msg]}
```

#### Module Options

Module options define the configurable parameters for a module. Each option has several properties:

- **widget_type**: The type of input widget (entry, checkbox, radiobutton, etc.)
- **required**: Whether the option is required
- **default**: The default value for the option
- **desc**: A description of the option
- **values**: For radiobutton and listbox types, the available values
- **min/max**: For scale and spinbox types, the minimum and maximum values

#### Internationalization

Modules should use the internationalization system for user-facing strings. This allows the module to be used in different languages without code changes.

#### Module Placement

Custom modules should be placed in the appropriate category directory under `xcore_framework/modules/`. For example, a module for image processing might be placed in `xcore_framework/modules/creative/`.

### Using the Module Creator

The XCORE Framework includes a graphical tool for creating modules, located at `dev/tools/module_creator.py`. This tool simplifies the process of creating new modules by providing a user-friendly interface for defining module metadata, options, and internationalization strings.

#### Starting the Module Creator

To start the Module Creator, run:

```bash
python dev/tools/module_creator.py
```

#### Key Features

- **Graphical Interface**: No need to write code manually
- **Module Metadata**: Define name, description, author, and version
- **Option Management**: Add, edit, and remove module options
- **Widget Type Selection**: Choose from various input widget types
- **Internationalization Support**: Automatically generate translation files
- **Code Generation**: Generate module code based on the defined metadata and options

#### Using the Module Creator

1. **Enter Module Metadata**:
   - Module Name: The name of the module (used for the module path)
   - Description: A brief description of the module
   - Author: Your name or organization
   - Version: The module version (default: 1.0.0)
   - Save Path: Where to save the generated module file

2. **Add Module Options**:
   - Name: The option name (used in the code)
   - Default: The default value
   - Description: A description of the option
   - Widget Type: The type of input widget
   - Required: Whether the option is required
   - Additional properties based on the widget type (values, min/max, etc.)

3. **Add Translation Sentences**:
   - Enter sentences that will be automatically added to the translation files
   - These sentences will be accessible through the i18n system

4. **Generate the Module**:
   - Click "Generate Module" to create the module file and translation files
   - The module will be saved to the specified path
   - Translation files will be created in the appropriate language directories

#### Translation Support

The Module Creator automatically generates translation files for both German and English. It uses the Google Translate API to translate strings from German to English, ensuring that your module is accessible to users of both languages.

## Internationalization

The XCORE Framework includes a comprehensive internationalization (i18n) system that allows the application to be used in different languages. Currently, German and English are supported.

### Language Files

Translation strings are stored in JSON files in the `xcore_framework/config/i18n/<language_code>/` directories. Each module or component can have its own translation file.

### Using Translations

To use translations in code, import the i18n object and use the `t` method:

```python
from xcore_framework.config.i18n import i18n

# Get a translation string
translated_string = i18n.t("key.subkey")

# Get a translation with variable substitution
translated_string = i18n.t("key.subkey", variable=value)
```

### Changing the Language

To change the language at runtime, use the `set_language` method:

```python
from xcore_framework.config.i18n import i18n

# Change to English
i18n.set_language('en')

# Change to German
i18n.set_language('de')
```

### Adding New Translations

To add translations for a new module:

1. Create JSON files in the language directories
2. Add translation keys and values for each language
3. Use the keys in your module code

The Module Creator tool can automate this process for new modules.

## Configuration

The XCORE Framework uses environment variables for configuration. These variables can be set in the `.env` file or through the Setpoint Mode.

### Environment Variables

Key environment variables include:

- `XCORE_FRAMEWORK`: Path to the framework directory
- `XCORE_ENV`: Path to the .env file
- `XCORE_CONFIG`: Path to the configuration directory
- `XCORE_I18N`: Path to the internationalization directory
- `XCORE_CORE`: Path to the core directory
- `XCORE_MODULES`: Path to the modules directory
- `XCORE_DATABASE`: Path to the database directory
- `XCORE_WEB_INTERFACE_DIR`: Path to the web interface directory
- `XCORE_WEB_INTERFACE_URL`: URL for the web interface
- `XCORE_LANGUAGE`: Default language for the framework

### Configuration Management

The Setpoint Mode provides a user-friendly interface for managing these configuration variables. See the [Setpoint Mode](#setpoint-mode) section for details.

## Development

### Setting Up a Development Environment

1. Clone the repository
2. Install dependencies
3. Set up environment variables
4. Run the application in the desired mode

### Development Workflow

1. Make changes to the code
2. Test changes in the appropriate mode
3. Update documentation if necessary
4. Submit a pull request

### Adding New Features

New features should be implemented as modules whenever possible. This keeps the core framework clean and maintainable.

## Vision

The XCORE Framework is a project with significant development potential. This vision outlines future development possibilities and improvements that could be implemented over time.

### Web Security

- Implementation of advanced security measures for the web interface
- HTTPS support with automatic certificate management
- Enhanced authentication and authorization
- Protection against common web attack vectors (XSS, CSRF, SQL injection)
- Security audits and penetration testing

### Web Component Optimization

- Performance optimization of React components
- Implementation of code splitting and lazy loading
- Improved user experience through optimized loading times
- Responsive design improvements for various devices
- Accessibility according to WCAG standards

### SCSS/CSS Optimization

- Transition to SCSS for better maintainability
- Implementation of a consistent design system
- Optimization of CSS selectors for better performance
- Reduction of CSS file size through minification
- Improved animations and transitions

### GUI Development in PyQT

- Reimplementation of the GUI with PyQT for improved performance
- Consistent design across all operating systems
- Advanced user interface features
- Enhanced graphics support
- Customizable themes and layouts

### Extended Save and Load Functions

- Integration of save and load functions in all operating modes
- Support for various file formats (JSON, YAML, XML)
- Automatic backup and restoration of sessions
- Cloud synchronization of configurations and results
- Versioning of saved data

### Module Export and Integration

- Export of modules as standalone service units
- System integration of modules for automated execution
- Combination of different modules into complex workflows
- API interfaces for external applications
- Containerization of modules for easy deployment

### Personal Note

The XCORE Framework is a project that was created out of the joy of development and is not being developed in a professional context. There is certainly a lot of optimization potential in various areas of the project, and I am grateful for any feedback and help.

As a hobby project, the framework develops at a pace that is compatible with my available time. I welcome contributions, suggestions, and feedback from the community to continuously improve and expand the project.

## Contributing

Contributions to the XCORE Framework are welcome! Here are some ways you can contribute:

1. **Report Bugs**: Create an issue in the GitHub repository if you find a bug
2. **Suggest Features**: Have an idea for a new feature? Create an issue with your suggestion
3. **Contribute Code**: Fork the repository, make your changes, and create a pull request
4. **Create Modules**: Create new modules to extend the framework's functionality
5. **Improve Documentation**: Help improve the documentation to make the framework more accessible

## License

- **Code**: MIT License – see [LICENSE](https://github.com/x404bjrn/XCORE/blob/main/LICENSE) for details
- **Media Content**: CC BY 4.0 – see [Creative Commons](https://creativecommons.org/licenses/by/4.0/) for details

---

## written on the dark side of toast 🍞🌚  
#### © 2025, Xeniorn | [`x404bjrn`](https://github.com/x404bjrn)
