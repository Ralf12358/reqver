# reqver# reqver

A command-line tool to add version information to requirements.txt files.

## Usage

```
reqver <params> files
```

For more information, please refer to the documentation.
# reqver

A command-line tool to add version information to requirements.txt files.

## Installation

```
pip install reqver
```

## Usage

```
reqver [OPTIONS] [FILES]...
```

If no files are given, reqver looks for requirements.txt in the current directory. If not found, it searches parent directories. If still not found, it displays an error message.

### Options:

- `--force`: Force update of all package versions, even if they already have version information.

### Examples:

1. Process requirements.txt in the current directory:
   ```
   reqver
   ```

2. Process a specific requirements file:
   ```
   reqver path/to/requirements.txt
   ```

3. Process multiple requirements files:
   ```
   reqver req1.txt req2.txt
   ```

4. Force update all versions:
   ```
   reqver --force requirements.txt
   ```

## Behavior

For each specified file (or the found requirements.txt):

1. Treats it as a requirements file (if it is a text file).
2. For each requirement in the file:
   - If version info is present: leaves it as is, unless the `--force` option is set.
   - If no version info is present: gets the current version with pip.
3. Creates a backup of the old requirements file.
4. Writes the new requirements file with updated version information.