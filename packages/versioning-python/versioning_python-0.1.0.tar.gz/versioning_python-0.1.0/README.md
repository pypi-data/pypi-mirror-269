# pyv

pyv is a command-line interface (CLI) application for managing versioning in a using Python.

It correspond to a versionning plan explained in the [versionning_plan](./docs/api-versioning-strat.md)

## Installation

1. From pypi:

  ```bash
  pip install pyv
  ```

1. Clone the repository:

  ```bash
  git clone https://github.com/your-username/pyv.git
  
  # Navigate to the project directory:
  cd versioning-cli
  
  # Install the required dependencies:
  pip install -r requirements.txt
  ```

## Versioning App Usage

Run the CLI app using the following command format:

```bash
pyv app --dev <dev_subversion> --prod <prod_subversion> <action> [--level <level>]
```

Replace `<dev_subversion>` with the dev subversion in the format `Vx.y.z` , and `<prod_subversion>` with the prod subversion in the format `Vx.y.z`. The `<action>` parameter can be either `post_prod` or `push_prod`. The optional `--level` parameter specifies the level for the post_prod action (default: 1).

- initialize the state as:
  - dev subversion: V{n}.0.0: for example V2.0.0
  - prod subversion (not_required if n==0): V{n-1}.p.q
- actions
  - post_prod: return the version to create V{n-1}.(p+1).q if --level=1 or V{n-1}.p.(q+1) --level=1 (1 by default)
  - push_prod: return the version to create V{n+1}.0.0

If you have cloned the repository, instead, use `python pyv/main.py` instead of `pyv`

## Examples

```bash
pyv app --dev V3.0.0 --prod V1.2.3 push_prod --level 2
```

```bash
pyv app --dev V2.0.0 --prod V1.2.3 post_prod --level 2
```

other examples:

```bash
$ pyv app --dev V3.0.0 --prod V1.2.3 push_prod --level 2
>> error: V3 do not follow V1

$ pyv app --dev V3.0.0 push_prod --level 2
>> error: if prod is not set dev should be V0.0.0 or V1.0.0

$ pyv app --dev V2.0.0 --prod V1.2.3 post_prod --level 2
>> your new version V1.2.4

$ pyv app --dev V2.0.0 --prod V1.2.3 push_prod --level 2
>> your new version V3.0.0
```

## AutoVersioning Usage

Run the CLI app using the following command format:

```bash
pyv auto <repo_path>
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
