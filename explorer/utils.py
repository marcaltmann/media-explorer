import tomllib
from pathlib import Path

def get_project_version(base_dir: Path) -> str:
    pyproject_toml_file = base_dir / "pyproject.toml"
    with open(pyproject_toml_file, "rb") as f:
        data = tomllib.load(f)

    if "project" in data and "version" in data["project"]:
        version = data["project"]["version"]
    else:
        version = "unknown"

    return version
