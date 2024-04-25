import re
from pathlib import Path
from random import SystemRandom
from sys import stderr


def fail(msg):
    """
    In case of failure, display a message and exit(1)
    """
    print(msg, file=stderr)  # noqa: T201
    exit(1)


def vary_name(name: str):
    """
    Validates the name and creates variations
    """
    snake = re.match(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$", name)

    if not snake:
        fail("The project name is not a valid snake-case Python variable name")

    camel = [x[0].upper() + x[1:] for x in name.split("_")]

    return {
        "project_name_snake": name,
        "project_name_camel": "".join(camel),
        "project_name_readable": " ".join(camel),
    }


def make_random_key() -> str:
    """
    Generates a secure random string
    """
    r = SystemRandom()
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_+/[]"

    return "".join([r.choice(allowed) for _ in range(0, 50)])


def make_dir_path(project_dir, root, project_name) -> Path:
    """
    Generates the target path for a directory
    """
    root = str(root).replace("__project_name_snake__", project_name)
    real_dir = Path(project_dir).absolute()
    return real_dir / root


def make_file_path(project_dir, project_name, root, name) -> Path:
    """
    Generates the target path for a file
    """
    return make_dir_path(project_dir, root, project_name) / name


def generate_vars(project_name, project_dir):
    """
    Generates the variables to replace in files
    """
    out = vary_name(project_name)
    out["random_key"] = make_random_key()
    out["settings_file"] = make_file_path(
        project_dir,
        project_name,
        Path("src") / project_name,
        "settings.py",
    )

    return out


def get_files():
    """
    Read all the template's files
    """
    files_root = Path(__file__).parent / "files"

    for file_path in files_root.rglob("*"):
        if file_path.is_file():
            rel_path = file_path.relative_to(files_root)
            rel_root = rel_path.parent
            file_name = rel_path.name

            try:
                with file_path.open(encoding="utf-8") as f:
                    yield rel_root, file_name, f.read(), True
            except UnicodeError:
                with file_path.open("rb") as f:
                    yield rel_root, file_name, f.read(), False


def check_target(target_path):
    """
    Checks that the target path is not empty
    """
    target = Path(target_path)
    if not target.exists():
        return

    for entry in target.iterdir():
        if not entry.name.startswith("."):
            fail(f'Target directory "{target_path}" is not empty')


def replace_content(content, project_vars):
    """
    Replaces variables inside the content.
    """
    for k, v in project_vars.items():
        content = content.replace(f"__{k}__", str(v))

    return content


def copy_files(project_vars, project_dir, files):
    """
    Copies files from the template into their target location. Unicode files
    get their variables replaced here and files with a shebang are set to be
    executable.
    """
    for root, name, content, is_unicode in files:
        project_name = project_vars["project_name_snake"]

        if is_unicode:
            content = replace_content(content, project_vars)

        file_path = make_file_path(project_dir, project_name, root, name)
        make_dir_path(project_dir, root, project_name).mkdir(
            parents=True, exist_ok=True
        )

        if is_unicode:
            file_path.write_text(content, encoding="utf-8")

            if content.startswith("#!"):
                file_path.chmod(0o755)
        else:
            file_path.write_bytes(content)


def main(args):
    project_vars = generate_vars(args.project_name, args.dir)
    check_target(args.dir)
    copy_files(project_vars, args.dir, get_files())
