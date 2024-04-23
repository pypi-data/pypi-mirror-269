import argparse
import re
from typing import Union


def is_valid_version(version):
    pattern = r"^v\d+\.\d+\.\d+$"
    return re.match(pattern, version) is not None


def initialize_state(dev_version, prod_version):
    if dev_version:
        if not is_valid_version(dev_version):
            raise ValueError(
                "Invalid dev version format. Use pattern v{int}.{int}.{int}"
                + f" found instead {dev_version}"
            )
        dev_major = int(dev_version[1])
        if dev_version != f"v{dev_major}.0.0":
            raise ValueError(
                "Invalid dev version format. Use pattern v{int}.0.0"
                + f" found instead {dev_version}"
            )

    if prod_version:
        if not is_valid_version(prod_version):
            raise ValueError(
                "Invalid prod version format. Use pattern v{int}.{int}.{int}"
                + f" found instead {prod_version}"
            )
        prod_major = int(prod_version[1])

    if dev_version and prod_version:
        if prod_major + 1 != dev_major:
            raise ValueError(
                f"Invalid versions majors. 1 + {prod_major}(prod_major) = {1+prod_major} != {dev_major}(dev_major)"
            )
    elif dev_version:
        # no prod sent
        print("premiere mise en production non faite")
        if dev_major not in [0, 1]:
            raise ValueError(f"for the first prod, dev_majour should be 0 or 1. found {dev_major}")
    elif prod_version:
        # no dev send
        print("app in prod but no dev created yet")
        raise ValueError(
            f"dev branch not sent: please create(v{prod_major+1}.0.0) or send the dev branch v{prod_major+1}."
            + "{int}.{int}"
        )
    else:
        raise ValueError(f"please send dev and prod subversions")

    dev_subversion = (int(dev_version[1]), int(dev_version[3]), int(dev_version[5]))
    if prod_version:
        prod_subversion = (int(prod_version[1]), int(prod_version[3]), int(prod_version[5]))
    else:
        prod_subversion = None

    return dev_subversion, prod_subversion


def resolve_level(level: Union[str, int]):
    level_map = {
        "patch": 1,
        "minor": 2,
    }
    if level in level_map.values():
        return level
    if not level in level_map:
        raise ValueError(
            f"level = {level}({type(level)}) is not one of {tuple(level_map.keys())} or {tuple(level_map.values())}"
        )
    return level_map.get(level)


def _clean_env(version):
    print(f"> before everything, add, commit and push with no stash or conflict unsolved")
    print(f"  $ git checkout {version}")
    print(f'  $ git commit -m "msg" && git push origin {version}')
    print(f"> sync to recognize all remotes branches into the local")
    print(f"  $ git fetch")
    print(f"> and to verify")
    print(f"  $ git branch -r")


def create_new_branch_from_older(older_branch, new_branch, log=True):
    if log:
        print(f"> create the new branch {new_branch} from the old one {older_branch}")
    print(f"  $ git checkout -b {new_branch} {older_branch}")
    print(f"  $ git push --set-upstream origin {new_branch}")
    print(f"> backup the lock file of {older_branch}")
    print(f"  $ cp ./package-lock.json lock_files/package-lock.json.{older_branch}.bak")
    print(f"> to then be able run npm install only from the `package-lock.json` file")
    print(f"  $ cp lock_files/package-lock.json.{older_branch}.bak ./package-lock.json")
    print(f"  $ npm install --frozen-lockfile")


def _sync_modifs(to_header_version, from_version, label):
    ## handle prod header
    print(f"> make sure {label} header version {to_header_version} exists. if it doesnt, create it")
    print(f"  $ git checkout {from_version}")
    create_new_branch_from_older(from_version, to_header_version, log=False)

    ## sync sub_version to prod_header
    print(f"> sync modifs from {from_version} to {to_header_version}")

    print(
        f" > way1: merge from online repo: useful if versions are handled in different folders (local repo) as git fetch wont pull all branches"
    )
    print(f"  $ git checkout {to_header_version}")
    print(f"  $ git fetch")  # get record on modifs that happened on other branhed
    print(f"  $ git merge origin/{from_version}")

    print(f" > way2: merge from local repo")
    print(f"  $ git checkout {from_version}")
    print(f"  $ git pull origin {from_version}")
    print(f"  $ git checkout {to_header_version}")
    print(f"  $ git merge {from_version}")


def _clean_prod_modifs(prod_version, prod_subversion, push_dev=True):
    # clean env
    _clean_env(prod_version)
    prod_header_version = f"v{prod_subversion[0]}"
    _sync_modifs(prod_header_version, prod_version, label="prod")

    if push_dev:
        # handle dev header
        dev_header_version = f"v{prod_subversion[0] + 1}"
        _sync_modifs(dev_header_version, prod_header_version, label="dev")

    return prod_header_version


def update_current_major_version(prod_version, prod_subversion, level):
    prod_major = prod_subversion[0]
    prod_minor = prod_subversion[1]
    prod_patch = prod_subversion[2]

    if level == 3:
        raise ValueError("post prod changes dont include creation of new major version")
    elif level not in [1, 2]:
        assert 0

    # sync prod_version into prod_header then dev
    prod_header_version = _clean_prod_modifs(prod_version, prod_subversion, push_dev=True)

    if level == 1:
        new_v = f"v{prod_major}.{prod_minor}.{prod_patch+1}"
    elif level == 2:
        new_v = f"v{prod_major}.{prod_minor+1}.0"

    ## create the new one
    create_new_branch_from_older(prod_header_version, new_v)

    return new_v


def deploy_new_major_version(dev_version, dev_subversion, prod_version, prod_subversion):
    dev_major = dev_subversion[0]
    dev_minor = dev_subversion[1]
    dev_patch = dev_subversion[2]

    # sync dev_version into dev_header
    dev_header_version = _clean_prod_modifs(dev_version, dev_subversion, push_dev=False)

    if prod_subversion:
        # sync prod_version into prod_header then dev
        prod_header_version = _clean_prod_modifs(prod_version, prod_subversion, push_dev=True)
        old_prod_header_version = f"v{prod_subversion[0]}"
        assert old_prod_header_version == prod_header_version
        print(
            f"> {old_prod_header_version} and his subversions like {prod_version} should not be changed anymore"
        )
    new_prod_header_version = f"v{dev_major}"
    assert new_prod_header_version == dev_header_version

    new_dev_header_version = f"v{dev_major+1}"
    new_v = f"v{dev_major+1}.{0}.{0}"

    ## create the new one
    create_new_branch_from_older(dev_header_version, new_dev_header_version)
    create_new_branch_from_older(new_dev_header_version, new_v)

    return new_v


def build_versioning_parser(parser):
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
    parser.add_argument("--dev", required=False, help="Dev subversion (e.g., V2.0.0)")
    parser.add_argument("--prod", required=False, help="Prod subversion (e.g., V1.2.3)")
    parser.add_argument("action", choices=["post_prod", "push_prod"], help="Action to perform")
    parser.add_argument(
        "--level",
        type=int,
        default=1,
        choices=[1, 2, 3],
        help="Level for post_prod action (default: 1)",
    )
    return parser


def parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments.

    Returns
    -------
    argparse.Namespace
        The parsed command-line arguments.

    """
    parser = argparse.ArgumentParser(description="Versioning CLI App")
    parser = build_versioning_parser(parser)
    args = parser.parse_args()
    return args


def main(args: argparse.Namespace):
    try:
        dev_subversion, prod_subversion = initialize_state(args.dev, args.prod)

        level = resolve_level(args.level)

        if args.action == "post_prod":
            new_version = update_current_major_version(args.prod, prod_subversion, level)
        elif args.action == "push_prod":
            new_version = deploy_new_major_version(
                args.dev, dev_subversion, args.prod, prod_subversion
            )

        print(f"Your new version: {new_version}")

    except ValueError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    parsed_args = parse_args()
    main(args=parsed_args)
