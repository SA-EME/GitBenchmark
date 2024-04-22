from config import init_config
from arguments.index import parser

NAME="GitBenchmark"
VERSION="0.5.1"

def help_function():
    print(f"{NAME} {VERSION}")
    parser.print_help()

if __name__ == "__main__":
    init_config()
    parser.add_argument('--version', action='version', version=f"{NAME} {VERSION}")
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        help_function()