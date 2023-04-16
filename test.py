from datetime import datetime
import time
import os

from time import sleep
from rich.live import Live
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table

console = Console()

start_time = time.time()

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7))
    layout["main"].split_row(
        Layout(name="test"), Layout(name="solution1"), Layout(name="solution2"))
    # layout["side"].split(Layout(name="test"), Layout(name="solution1"), Layout(name="solution2"))
    return layout


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Stress-testings[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white")


i = 0

layout = make_layout()
layout["header"].update(Header())

with Live(layout, refresh_per_second=25, screen=True):
    while True:
        os.popen('python3 gen.py > test.txt')
        sleep(0.04)
        with open("test.txt", "r") as file:
            layout["test"].update(Panel(''.join(file.readlines()), border_style="red", title="Current test"))
        sleep(0.04)
        v2 = os.popen('./solution2 < test.txt').readlines()
        v1 = os.popen('./solution1 < test.txt').readlines()
        layout["solution1"].update(Panel(Align.center(''.join(v1)), border_style="blue", title="First solution answer"))
        layout["solution2"].update(Panel(Align.center(''.join(v2)), border_style="green", title="Second solution answer"))
        t = int(time.time() - start_time)
        layout["footer"].update(Panel(Align.center(f"{t//3600:02}:{t//60%60:02}:{t%60:02}", vertical="middle"), title="Total time"))
        if v1 != v2:
            break
        i += 1
console.print(f"[bold red]Stress-testing stopped on test #{i+1}[/bold red]\nInput:")
with open("test.txt", "r") as file:
    console.print(f"{''.join(file.readlines())}")
