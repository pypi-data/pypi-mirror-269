# hash_rename
A quick Python tool to rename files in a folder to be prefixed with a hash of the file's contents.

## Usage

```bash
pip install hash_rename

hash_rename --help
hash_rename '<path_to_file>'

# or, if you have issues with PATH:
python3 -m hash_rename '<path_to_file>'
```

## Example

Say you have a folder with the following files:

```
file1.txt
file2.txt
file3.txt
```

Running the tool renames the files to:

```
90be47_file1.txt
dbd06c_file2.txt
a7b5b7_file3.txt
```

## License

[The Unlicense](https://unlicense.org)
