import argparse
from happypig import animals, saying, default_animal

def list_handler(pretty=False):
    if pretty:
        try:
            from tabulate import tabulate
        except ImportError:
            raise ValueError("please install tabulate via `pip install tabulate` or `pip install happypig[tab]`")
        
        headers = ["animal", "content"]
        data = [(animal["animal"], animal["content"]) for animal in animals]
        print(tabulate(data, headers=headers, tablefmt='grid'))
    else:
        for animal in animals:
            print(saying(animal["animal"], animal["content"]))

def run_handler(name, content):
    if not name:
        name = default_animal["animal"]
    if not content:
        for animal in animals:
            if name in animal["animal"]:
                content = animal["content"]
                break
        else:
            content = "default content"
    print(saying(name, content))


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--pretty", action="store_true", help="use tablate to print, need install tabulate")

    parser_b = subparsers.add_parser("run")
    parser_b.add_argument("-n", "--name", default="", help="animal name")
    parser_b.add_argument("-c", "--content", default="", help="animal saying")

    args = parser.parse_args()
    if args.command == "list":
        list_handler(args.pretty)
    else:
        run_handler(args.name, args.content)
