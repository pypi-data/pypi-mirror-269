from rich.console import Console
from rich.markdown import Markdown

console = Console()


def formatted_print(text):
    console.print(Markdown(text, code_theme="material"))
