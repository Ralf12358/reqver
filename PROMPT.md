A pip installable module:

reqver

A command line tool which add version information in requirements.txt

Usage Example:

```
reqver <params> files
```

If no files are given: Looks for requirements.txt in current directory if not found tries parent directories. if not found displays error message

for each file of files:
    Treat it as a requirements files (if it is a text file)
    For each requirement in the files:
        - if version info is present: leave it as is, except if "--force" command line param is set
        - if no version info is present. gets current version with "pip"
    Make as backup of the old requirements file (except: --no-backups is given)
    Writes the new one
