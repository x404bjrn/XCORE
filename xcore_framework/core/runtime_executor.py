# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
import os
import json
import tempfile
import subprocess
import importlib.util

from xcore_framework.config.env import RUNTIME_PACKAGE, DIRECTORY_WORKSPACE


def read_state_file(state_file, fallback_state):
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print("⚠️ state_file ist leer – ursprünglicher state wird verwendet.")
                return fallback_state
            return json.loads(content)
    except Exception as e:
        print(f"❌ Fehler beim Lesen von {state_file}: {e}")
        return fallback_state



class XCoreRuntimeExecutor:
    def __init__(self, working_dir: str = None):
        self.base_working_dir = working_dir or DIRECTORY_WORKSPACE
        os.makedirs(self.base_working_dir, exist_ok=True)

    SUFFIX_MAP = {
        "python": ".py",
        "bash": ".sh",
        "powershell": ".ps1",
        "java": ".java",
        "node": ".js",
    }

    def execute(self, section: dict, params: dict, state: dict, mode="cli", gui_console=None):
        lang = section["language"].lower()
        code = section["code"]

        params["_working_dir"] = self.base_working_dir

        if lang == "python":
            return self.run_python(code, params, state, mode, gui_console)

        elif lang == "bash":
            return self.run_bash(code, params, state)

        elif lang == "powershell":
            return self.run_powershell(code, params, state)

        elif lang == "java":
            return self.run_java(code, params, state)

        elif lang == "node":
            return self.run_node(code, params, state)

        else:
            raise ValueError(f"Nicht unterstützte Sprache: {lang}")


    def run_python(self, code, params, state, mode="cli", gui_console=None):
        with tempfile.NamedTemporaryFile(suffix=self.SUFFIX_MAP['python'], delete=False, mode="w") as temp:
            temp.write(code + "\n\nresult = run(params, state)")
            path = temp.name

        import io
        import sys
        old_stdout = sys.stdout
        stdout_buffer = io.StringIO()

        try:
            sys.stdout = stdout_buffer

            spec = importlib.util.spec_from_file_location("mod", path)
            mod = importlib.util.module_from_spec(spec)
            mod.params = params
            mod.state = state
            mod.mode = mode
            mod.gui_console = gui_console
            spec.loader.exec_module(mod)

            sys.stdout.flush()
            stdout_output = stdout_buffer.getvalue()

            updated_state = mod.result if isinstance(mod.result, dict) else state
            updated_state["__exec__"] = {
                "success": True,
                "returncode": 0,
                "stdout": stdout_output.strip(),
                "stderr": ""
            }
            return updated_state

        except Exception as e:
            sys.stdout.flush()
            stdout_output = stdout_buffer.getvalue()

            state["__exec__"] = {
                "success": False,
                "returncode": -1,
                "stdout": stdout_output.strip(),
                "stderr": str(e)
            }
            return state

        finally:
            sys.stdout = old_stdout
            stdout_buffer.close()
            os.unlink(path)


    def run_bash(self, code, params, state):
        from xcore_framework.core.runtime_manager import BashRuntimeManager
        bash_runtime = BashRuntimeManager()
        bash = bash_runtime.get_binary()

        return self._run_script_with_io(bash, code,
                                        f"script{self.SUFFIX_MAP['bash']}", params, state)


    def run_powershell(self, code, params, state):
        from xcore_framework.core.runtime_manager import PowerShellRuntimeManager
        ps_runtime = PowerShellRuntimeManager()
        ps = ps_runtime.get_binary()

        return self._run_script_with_io(ps, code,
                                        f"script{self.SUFFIX_MAP['powershell']}", params, state,
                                        ["-ExecutionPolicy", "Bypass", "-File"])


    def run_java(self, code, params, state):
        tempdir = tempfile.mkdtemp()
        java_file = os.path.join(tempdir, f"Main{self.SUFFIX_MAP['java']}")
        with open(java_file, "w", encoding="utf-8") as f:
            f.write(code)

        param_file = os.path.join(tempdir, "params.json")
        state_file = os.path.join(tempdir, "state.json")
        with open(param_file, "w") as f: json.dump(params, f)
        with open(state_file, "w") as f: json.dump(state, f)

        from xcore_framework.core.runtime_manager import JavaRuntimeManager
        java_runtime = JavaRuntimeManager()
        java, javac = java_runtime.get_binary()

        #javac = os.path.join(RUNTIME_PACKAGE['DIRECTORY_RUNTIMES'], "java", "jdk-20.0.2+9", "bin", "javac.exe")
        #java = os.path.join(RUNTIME_PACKAGE['DIRECTORY_RUNTIMES'], "java", "jdk-20.0.2+9", "bin", "java.exe")

        try:
            subprocess.run([javac, java_file], check=True, capture_output=True, text=True)
            result = subprocess.run(
                [java, "-cp", tempdir, "Main", param_file, state_file],
                capture_output=True, text=True
            )

            new_state = read_state_file(state_file, state)
            new_state["__exec__"] = {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
            return new_state

        except subprocess.CalledProcessError as e:
            state["__exec__"] = {
                "success": False,
                "returncode": e.returncode,
                "stdout": e.stdout.strip() if e.stdout else "",
                "stderr": e.stderr.strip() if e.stderr else str(e)
            }
            return state


    def run_node(self, code, params, state):
        from xcore_framework.core.runtime_manager import NodeRuntimeManager
        node_runtime = NodeRuntimeManager()
        node = node_runtime.get_binary()

        return self.run_simple(node, code, params, state)


    def run_simple(self, interpreter, code, params, state):
        return self._run_script_with_io(interpreter, code, "script", params, state)


    def _run_script_with_io(self, interpreter, code, filename, params, state, pre_args=None):
        tempdir = tempfile.mkdtemp()
        script_path = os.path.join(tempdir, filename)
        param_file = os.path.join(tempdir, "params.json")
        state_file = os.path.join(tempdir, "state.json")

        with open(script_path, "w", encoding="utf-8") as f: f.write(code)
        with open(param_file, "w") as f: json.dump(params, f)
        with open(state_file, "w") as f: json.dump(state, f)

        try:
            args = [interpreter]
            if pre_args:
                args.extend(pre_args)
            args.append(script_path)
            args.extend([param_file, state_file])

            result = subprocess.run(args, capture_output=True, text=True)

            new_state = read_state_file(state_file, state)
            new_state["__exec__"] = {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
            return new_state

        except subprocess.CalledProcessError as e:
            state["__exec__"] = {
                "success": False,
                "returncode": e.returncode,
                "stdout": e.stdout.strip() if e.stdout else "",
                "stderr": e.stderr.strip() if e.stderr else str(e)
            }
            return state
