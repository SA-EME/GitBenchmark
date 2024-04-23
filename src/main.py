from config import config
from rich import print

from arguments.index import parser, COMMAND_WITHOUT_CONFIG

NAME="GitBenchmark"
VERSION="0.6.2"

def help_function():
    print(f"{NAME} {VERSION}")
    parser.print_help()

if __name__ == "__main__":
    parser.add_argument('--version', action='version', version=f"{NAME} {VERSION}")
    args = parser.parse_args()
    if args.command not in COMMAND_WITHOUT_CONFIG and config is None:
        print("[red]Aucune configuration trouvée, utilisée gb init.[/red]")
    elif 'func' in args:
        args.func(args)
    else:
        help_function()