import argparse

from pyv.core.auto_versionning import build_autoversioning_parser
from pyv.core.auto_versionning import main as autoversioning_main
from pyv.core.versionning import build_versioning_parser
from pyv.core.versionning import main as versioning_main


def create_parser() -> argparse.ArgumentParser:
    """
    Create an ArgumentParser for the versioning.

    Returns:
    -------
    argparse.ArgumentParser:
        The ArgumentParser object for the versioning.
    """
    parser = argparse.ArgumentParser(description="Versioning Application")
    subparsers = parser.add_subparsers(dest="command", help="Select the component to run")

    # Subparser for the versioning
    versioning_parser = subparsers.add_parser("app", help="Run the versioning versioning")

    # versioning-specific arguments
    versioning_parser = build_versioning_parser(versioning_parser)

    # Subparser for the autoversioning
    autoversioning_parser = subparsers.add_parser(
        "auto", help="Run the git based autoversioning tool"
    )

    # versioning-specific arguments
    autoversioning_parser = build_autoversioning_parser(autoversioning_parser)

    return parser


def main():
    """
    Main function to execute the versioning.

    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "app":
        versioning_main(args)
    elif args.command == "auto":
        autoversioning_main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
