import subprocess
import sys
import threading

from langchain.agents import Tool
from langchain_core.tools import BaseTool, ToolException
from zrb.helper.accessories.color import colored
from zrb.helper.typing import Any, List

from ...task.any_prompt_task import AnyPromptTask
from ..schema import ToolFactory


def python_repl_tool_factory(
    name: str = "Python Code Runner",
    description: str = "Use this tool to execute a Python Code. The input should be a valid and complete Python Code that doesn't require user intervention.",  # noqa
) -> ToolFactory:
    def create_python_repl_tool(task: AnyPromptTask) -> BaseTool:
        return Tool(
            name=task.render_str(name),
            description=task.render_str(description),
            func=_eval_python,
            handle_tool_error=True,
        )

    return create_python_repl_tool


def _eval_python(script: str):
    sanitized_python_script = _sanitize_python_script(script)
    process = subprocess.Popen(
        ["python", "-c", sanitized_python_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout_lines, stderr_lines = [], []
    stdout_thread = threading.Thread(
        target=_print_stream, args=(process.stdout, stdout_lines)
    )
    stderr_thread = threading.Thread(
        target=_print_stream, args=(process.stderr, stderr_lines)
    )
    stdout_thread.start()
    stderr_thread.start()
    process.wait()
    stdout_thread.join()
    stderr_thread.join()
    if process.returncode != 0:
        raise ToolException("".join(stderr_lines))
    return "".join(stdout_lines)


def _sanitize_python_script(script: str) -> str:
    script = _sanitize_multiline_python_script(script)
    if "\n" not in script and script[0] == "`" and script[-1] == "`":
        return script[1:-1]
    return script


def _sanitize_multiline_python_script(script: str) -> str:
    script = script.lstrip().rstrip()
    if "```" in script:
        lines = script.split("\n")
        is_code = False
        script_lines = []
        for line in lines:
            if not is_code and (line == "```python" or line == "```"):
                is_code = True
                continue
            if is_code and line == "```":
                break
            if is_code:
                script_lines.append(line)
        return "\n".join(script_lines)
    return script


def _print_stream(stream: Any, lines: List[str]):
    while True:
        line = stream.readline()
        if not line:
            break
        print(colored(line, attrs=["dark"]), end="", file=sys.stderr, flush=True)
        lines.append(line)
