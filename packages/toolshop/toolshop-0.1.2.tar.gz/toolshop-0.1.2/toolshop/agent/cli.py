import click
from .coder import Coder

@click.group(invoke_without_command=True)
@click.pass_context
def coder(ctx):
    """Coder Command Line Interface"""
    if ctx.invoked_subcommand is None:
        start()

@coder.command()
def start():
    "Start the chat with Coder."
    app = Coder(coder_is_interactive=True)
    app.chat()

@coder.command()
def do(instructions: str):
    "Send instructions for Coder to execute non-interactively."
    app = Coder(coder_is_interactive=False)
    app.do(instructions)
