[![DE](https://img.shields.io/badge/DE-blue?style=for-the-badge)](https://github.com/x404bjrn/XCORE/blob/main/CONTRIBUTING.md)
![EN](https://img.shields.io/badge/EN-green?style=for-the-badge)

# 🤝 Contributing to XCORE-Framework

---

Thank you for your interest in contributing to the **XCORE-Framework**!  
This project is still in active development – all kinds of contributions are welcome, whether it's code, testing, documentation, or just feedback.

---

## 📋 Table of Contents

1. [How to Contribute](#-how-to-contribute)
2. [Ground Rules](#-ground-rules)
3. [Local Setup](#-local-setup)
4. [Issues & Pull Requests](#-issues--pull-requests)
5. [Code Style](#-code-style)
6. [Contact](#-contact)

---

## ✅ How to Contribute

You can help in many ways:

- 🔧 **Report bugs**
- 💡 **Suggest new features**
- 🛠️ **Contribute code** (modules, enhancements)
- 🧪 **Write tests**
- 📚 **Improve documentation**
- 🌍 **Add or improve translations**

---

## 📌 Ground Rules

- Be friendly and respectful on all platforms.
- Use `issues` to discuss ideas, bugs, or questions.
- Write clear and meaningful commit messages (e.g., use `feat:`, `fix:`, `docs:` prefixes).
- Follow the existing project style – keep the code readable and clean.

---

## 🛠️ Local Setup

If you want to contribute locally:

### Clone the project

```
git clone https://github.com/x404bjrn/XCORE.git
cd XCORE
```

### Recommended: PDM (Python Dependency Manager)
PDM is the preferred tool for managing dependencies in this project. It provides better isolation, more accurate dependency management, and simplifies development workflows.

#### Install PDM (if not already installed)
```
pip install pdm
```

#### Install dependencies with PDM
```
pdm install
```

#### Activate PDM environment
```
# For a single shell session
pdm run <command>

# Or start a new shell with PDM environment activated
pdm shell
```

#### Useful PDM commands
```
pdm add <package>        # Add a new dependency
pdm remove <package>     # Remove a dependency
pdm update               # Update all dependencies
pdm run tests            # Run tests
pdm run export-req       # Generate requirements.txt
```

### Alternative: Classic virtual environment
If you prefer not to use PDM:
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### (Optional) Set up frontend

```
cd dev/frontend/web
npm install
npm run dev
```

## 🔄 Issues & Pull Requests

- Please open an issue before making big changes.
- Fork the repo and work on a separate branch (`feature/your-topic`).
- Write a clear and descriptive pull request.
- Avoid unnecessary commits like `fix typo` or `test123`.
- Test your changes locally before submitting.

## 🎨 Code Style

- Python: PEP8-compliant (e.g. via `black`, `mypy`, `flake8`)
- React: Keep components clean and consistent
- Comment where the code is not self-explanatory
- Use English for all variable and function names

## 📬 Contact

Got questions or want to give feedback?

- GitHub Issues or Discussions
- Email: [void@insomnialegion.xyz](mailto:void@insomnialegion.xyz)
