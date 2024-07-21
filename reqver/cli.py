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

def process_requirements_file(file_path, force=False, no_backups=False):
    click.echo(f"Processing {file_path}...")
    with open(file_path, 'r') as f:
        requirements = f.readlines()

    updated_requirements = []
    changes_made = False
    for req in requirements:
        req = req.strip()
        if req and not req.startswith('#'):
            splitted = re.split(r'==|>=|<=|<|>', req)
            package_name = splitted[0].strip()
            old_version = splitted[1].strip() if len(splitted) > 1 else None
            version = get_package_version(package_name)
            print(f"package_name: {package_name} old_version: {old_version} version: {version}")
            if version:
                if old_version is None or (force and version != old_version):
                    updated_requirements.append(f"{package_name}=={version}\n")
                    changes_made = True
                    if old_version:
                        click.echo(f"  {package_name}: {old_version} -> {version}")
                    else:
                        click.echo(f"  {package_name}: added version {version}")
                else:
                    updated_requirements.append(req + '\n')
            else:
                updated_requirements.append(req + '\n')
        else:
            updated_requirements.append(req + '\n')

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
