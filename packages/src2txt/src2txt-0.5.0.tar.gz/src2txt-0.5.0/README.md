# README for src2txt

## Overview

`src2txt` is a command-line tool designed to convert various types of documents and web pages into plain text. It supports processing local files (including PDFs and HTML files) and web URLs. The tool provides options for recursive directory processing, inclusion of hidden files, and can respect `.gitignore` rules.

## Features

- Convert files and URLs to text.
- Support for multiple file types including text, HTML, and PDF.
- Recursive processing of directories.
- Options to include hidden files and ignore `.gitignore` rules.
- Verbose output and listing files without processing.

## Installation

### Using pipx

The recommended method to install `src2txt` is using `pipx`, which installs Python applications in isolated environments. To install `src2txt` using `pipx`, run:

```bash
pipx install src2txt
```

If `pipx` is not installed, you can install it via pip:

```bash
pip install pipx
pipx ensurepath
```

## Usage

To use `src2txt`, you can invoke it from the command line with various options. Here’s a basic example:

```bash
src2txt src_to_text --sources "path/to/file_or_directory" --recursive
```

### Command Line Options

- `--sources`: List of file paths or URLs.
- `--raw-html`: Return raw HTML content without cleaning.
- `--recursive`: Recursively process files in directories.
- `--include-hidden`: Include hidden files in the processing.
- `--ignore-gitignore`: Ignore `.gitignore` rules and include files normally ignored.
- `--verbose`: Print verbose output.
- `--file-name`: Print the file name or URL before the content.
- `--list`: List files and URLs without processing content.

For more detailed usage and options, refer to the help provided by the tool:

```bash
src2txt --help
```

## Contributing

Contributions to `src2txt` are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
