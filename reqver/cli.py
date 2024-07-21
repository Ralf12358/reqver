import click
import os
import re
import subprocess
import shutil
from pathlib import Path

def find_requirements_file():
    current_dir = Path.cwd()
    while current_dir != current_dir.root:
        req_file = current_dir / "requirements.txt"
        if req_file.exists():
            return req_file
        current_dir = current_dir.parent
    return None

def get_package_version(package_name):
    try:
        result = subprocess.run(["pip", "show", package_name], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith("Version:"):
                    return line.split(":")[1].strip()
    except Exception:
        pass
    return None

def process_requirements_file(file_path, force=False):
    with open(file_path, 'r') as f:
        requirements = f.readlines()

    updated_requirements = []
    for req in requirements:
        req = req.strip()
        if req and not req.startswith('#'):
            package_name = re.split('[=<>]', req)[0]
            if force or '==' not in req:
                version = get_package_version(package_name)
                if version:
                    updated_requirements.append(f"{package_name}=={version}\n")
                else:
                    updated_requirements.append(req + '\n')
            else:
                updated_requirements.append(req + '\n')
        else:
            updated_requirements.append(req + '\n')

    # Create backup
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
    shutil.copy2(file_path, backup_path)

    # Write updated requirements
    with open(file_path, 'w') as f:
        f.writelines(updated_requirements)

@click.command()
@click.option('--force', is_flag=True, help='Force update of all package versions')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(force, files):
    """Add version information to requirements.txt files."""
    if not files:
        req_file = find_requirements_file()
        if req_file:
            files = [req_file]
        else:
            click.echo("Error: No requirements.txt file found in the current or parent directories.")
            return

    for file in files:
        click.echo(f"Processing {file}...")
        process_requirements_file(Path(file), force)
        click.echo(f"Updated {file}")

if __name__ == '__main__':
    main()
