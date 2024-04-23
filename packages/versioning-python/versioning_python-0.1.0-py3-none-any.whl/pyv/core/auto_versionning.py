import argparse
import os
import re
import subprocess

from git import Repo
from git.exc import InvalidGitRepositoryError

from .utils import log_on_value_error, print_function_name

current_dir = os.path.dirname(os.path.abspath(__file__))
versionning_script_path = os.path.join(current_dir, "versionning.py")


def is_valid_version_branch(branch_name):
    pattern = r"^v\d+\.\d+\.\d+$"
    return re.match(pattern, branch_name) is not None


def list_version_branches(repo_path):
    # Check if the repository exists
    if not os.path.exists(repo_path):
        raise ValueError(f"Repository path '{repo_path}' does not exist.")

    # Check if it's a Git repository
    try:
        repo = Repo(repo_path)
    except InvalidGitRepositoryError:
        raise ValueError(f"'{repo_path}' is not a Git repository.")

    if not repo.git_dir:
        raise ValueError(f"'{repo_path}' is not a Git repository.")

    # Get the list of branches and filter the version branches
    branches = repo.git.branch("-r", "--list", "origin/*").splitlines()
    # print(branches)
    rmv_origin_txt = lambda x: x[7:]  # if x.startswith("origin/") else x
    version_branches = [
        rmv_origin_txt(branch.strip())
        for branch in branches
        if is_valid_version_branch(rmv_origin_txt(branch.strip()))
    ]

    return version_branches


@print_function_name
@log_on_value_error
def auto_versionning(repo_path):
    repo_path = os.path.abspath(repo_path)
    if not os.path.exists(repo_path):
        raise ValueError(f"repo_path {repo_path} doesn't exists")

    version_branches = sorted(list_version_branches(repo_path), reverse=True)
    if not version_branches:
        print(f"No version branches found in {repo_path}.")
        return

    print("> Version Branches:")
    for branch in version_branches:
        print("  ", branch)

    last_dev_branch = version_branches[0]
    last_prod_branch = [elt for elt in version_branches if not elt.startswith(last_dev_branch[:2])]
    last_prod_branch = last_prod_branch[0] if last_prod_branch else ""

    print(f"> last_dev_branch={last_dev_branch}")
    print(f"> last_prod_branch={last_prod_branch}")

    for action in ["push_prod", "post_prod"]:
        # Pushing to prod / Post production
        if last_dev_branch and last_prod_branch:
            _cmd = [
                "python",
                versionning_script_path,
                "--dev",
                last_dev_branch.lower(),
                "--prod",
                last_prod_branch.lower(),
                action,
                "--level",
                "2",
            ]
            subprocess.run(["echo", f"\n>>> Running: {' '.join(_cmd)}"], check=True)
            subprocess.run(_cmd, check=True)


def build_autoversioning_parser(parser):
    """
    Build versioning parser.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        The ArgumentParser object.

    Returns
    -------
    argparse.ArgumentParser
        The modified ArgumentParser object.

    """
    parser.add_argument("repo_path", help="Path to the local Git repository")
    return parser


def parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments.

    Returns
    -------
    argparse.Namespace
        The parsed command-line arguments.

    """
    parser = argparse.ArgumentParser(description="List Version Branches")
    parser = build_autoversioning_parser(parser)
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace):
    auto_versionning(args.repo_path)


if __name__ == "__main__":
    parsed_args = parse_args()
    main(args=parsed_args)
