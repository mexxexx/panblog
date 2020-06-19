import sys

from . import init
from . import sites
from . import make


def main():
    args = sys.argv[1:]

    try:
        if len(args) > 0:
            action = args[0]
            if action == "init":
                init.init()
                make.reload()
                sys.exit(0)
            elif action == "list":
                sites.list_sites(True)
                sys.exit(0)
            elif action == "add":
                sites.add_files(args[1:])
                make.reload()
                sys.exit(0)
            elif action == "remove":
                sites.remove_files(args[1:])
                make.reload()
                sys.exit(0)
            elif action == "reload":
                make.reload()
                sys.exit(0)
            elif action == "make":
                make.make()
                sys.exit(0)

        print_help()
    except ValueError as e:
        print(e)


def print_help():
    print("Help")


if __name__ == "__main__":
    main()
