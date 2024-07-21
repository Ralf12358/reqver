import click
import os
import re
import subprocess
import shutil
from pathlib import Path
from packaging import version
from packaging.specifiers import SpecifierSet

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

def process_requirements_file(file_path, force=False, no_backups=False):
    click.echo(f"Processing {file_path}...")
    with open(file_path, 'r') as f:
        requirements = f.readlines()

    updated_requirements = []
    changes_made = False
    for req in requirements:
        req = req.strip()
        if req and not req.startswith('#'):
            match = re.match(r'^([^=<>]+)\s*(==|>=|<=|<|>)?\s*(.*)$', req)
            if match:
                package_name, operator, old_version = match.groups()
                package_name = package_name.strip()
                current_version = get_package_version(package_name)
                if current_version:
                    if old_version and operator:
                        specifier = SpecifierSet(f"{operator}{old_version}")
                        if force and not specifier.contains(current_version):
                            updated_req = f"{package_name}=={current_version}\n"
                            changes_made = True
                            click.echo(f"  {package_name}: {old_version} -> {current_version}")
                        else:
                            updated_req = f"{req}\n"
                    else:
                        updated_req = f"{package_name}=={current_version}\n"
                        changes_made = True
                        click.echo(f"  {package_name}: added version {current_version}")
                    updated_requirements.append(updated_req)
                else:
                    updated_requirements.append(f"{req}\n")
            else:
                updated_requirements.append(f"{req}\n")
        else:
            updated_requirements.append(f"{req}\n")

    if changes_made:
        if not no_backups:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.bak')
            shutil.copy2(file_path, backup_path)
            click.echo(f"  Backup created: {backup_path}")

        # Write updated requirements
        with open(file_path, 'w') as f:
            f.writelines(updated_requirements)
        click.echo(f"  Updated {file_path}")
    else:
        click.echo("  No changes were necessary.")

@click.command()
@click.option('--force', is_flag=True, help='Force update of all package versions')
@click.option('--no-backups', is_flag=True, help='Do not create backup files')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(force, no_backups, files):
    """Add version information to requirements.txt files."""
    if not files:
        req_file = find_requirements_file()
        if req_file:
            files = [req_file]
        else:
            click.echo("Error: No requirements.txt file found in the current or parent directories.")
            return

    for file in files:
        process_requirements_file(Path(file), force, no_backups)

if __name__ == '__main__':
    main()
