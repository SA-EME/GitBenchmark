from rich import print

from config import init_config
from controllers.init import init

def init_arguments(args):
    if init_config() is None:
        init()
    else:
        print("[red]The configuration file already exists, you can remove it if you want to reinitialize it.[/red]")