from config import config
from rich import print

from arguments.index import parser, COMMAND_WITHOUT_CONFIG

from version import get_version
from utils import execute_command

NAME="GitBenchmark"
VERSION="0.8.1"

def help_function():
    print(f"{NAME} {VERSION}")
    parser.print_help()

def requirements():
    git = execute_command("git --version")

    git_version = get_version(git, r"(git version) (\d+\.\d+\.\d+)")

    if git_version is None:
        print("[red]Git n'est pas installé, veuillez l'installer")
        exit(1)

    print(f"[green]Git {git_version}[/green]")


if __name__ == "__main__":
    requirements()
    parser.add_argument('--version', action='version', version=f"{NAME} {VERSION}")
    args = parser.parse_args()
    if args.command not in COMMAND_WITHOUT_CONFIG and config is None:
        print("[red]Aucune configuration trouvée, utilisée gb init.[/red]")
    elif 'func' in args:
        args.func(args)
    else:
        help_function()