# norc/main.py
# MIT License © 2025 Wrydrick Gutierrez

from norc.cli import parser as cli_parser

def main():
    parser = cli_parser.build_parser()
    args = parser.parse_args()
    cli_parser.dispatch(args)
        
if __name__ == "__main__":
    main()