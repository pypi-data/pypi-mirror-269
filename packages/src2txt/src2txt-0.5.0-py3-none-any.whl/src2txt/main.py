import glob
import pathlib
import re

import fitz  # PyMuPDF
import magic
import pathspec
import requests
import typer
from bs4 import BeautifulSoup
from readability import Document
from rich import print

app = typer.Typer()


@app.command()
def src_to_text(
    sources: list[str] = typer.Argument(..., help="List of file paths or URLs."),
    raw_html: bool = typer.Option(
        False, "--raw-html", "-h", help="Return raw HTML content without removing html tags."
    ),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursively process files in directories."),
    include_hidden: bool = typer.Option(
        False, "--include-hidden", "-i", help="Include hidden files in the processing."
    ),
    ignore_gitignore: bool = typer.Option(
        False, "--ignore-gitignore", help="Ignore .gitignore rules and include files normally ignored."
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Print verbose output."),
    file_name: bool = typer.Option(False, "--file-name", "-f", help="Print the file name or URL before the content."),
    list_files: bool = typer.Option(False, "--list", "-l", help="List files and URLs without processing content."),
):
    """
    Convert a file, URL, or directory of files to text.

    This command allows you to extract text from specified sources, which can be either local files or URLs.

    """
    clean = not raw_html
    for src in sources:
        try:
            process_source(src, clean, recursive, include_hidden, ignore_gitignore, verbose, file_name, list_files)
        except ValueError as e:
            typer.echo(f"Error: {e}")


def process_source(src, clean, recursive, include_hidden, ignore_gitignore, verbose, file_name, list_files):
    """Determine the source type and process it accordingly."""
    if is_local_file(src):
        process_local_file(src, clean, recursive, include_hidden, ignore_gitignore, verbose, file_name, list_files)
    elif list_files:
        print(src)
    else:
        process_and_print(src, clean, verbose, file_name)


def process_local_file(src, clean, recursive, include_hidden, ignore_gitignore, verbose, file_name, list_files):
    """Process a local file or directory based on the provided parameters."""
    path = pathlib.Path(src)
    if path.is_dir():
        process_directory(path, clean, recursive, include_hidden, ignore_gitignore, verbose, file_name, list_files)
    else:
        process_files(glob.glob(src), clean, include_hidden, verbose, file_name, list_files)


def process_directory(path, clean, recursive, include_hidden, ignore_gitignore, verbose, file_name, list_files):
    """
    Process a directory of files based on the provided parameters.

    This function processes each file in the specified directory, applying filters for hidden files
    and .gitignore rules if specified. It either lists the files or processes them for text extraction
    based on the flags provided.
    """
    pattern = "**/*" if recursive else "*"
    files = list(path.rglob(pattern)) if recursive else list(path.glob(pattern))

    # Exclude .git directory by default
    files = [f for f in files if ".git" not in f.parts]

    if not include_hidden:
        files = [f for f in files if not any(part.startswith(".") for part in f.parts)]
    if not ignore_gitignore:
        gitignore_path = path / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path) as file:
                spec = pathspec.PathSpec.from_lines("gitwildmatch", file)
                files = [f for f in files if not spec.match_file(f)]
    for file in files:
        if file.is_file():
            if list_files:
                print(file)
            else:
                process_and_print(file, clean, verbose, file_name)


def process_files(files, clean, include_hidden, verbose, file_name, list_files):
    """Filter and process files based on visibility, listing preference, and other parameters."""
    if not include_hidden:
        files = [f for f in files if not any(part.startswith(".") for part in pathlib.Path(f).parts)]
    for file in files:
        file_path = pathlib.Path(file)
        if file_path.is_file():
            if list_files:
                print(file_path)
            else:
                process_and_print(file_path, clean, verbose, file_name)


def process_and_print(source, clean, verbose, file_name):
    """Process and print the content of the given source based on file location and type."""

    source_str = str(source) if isinstance(source, pathlib.Path) else source
    if file_name:
        print(f"---\n{source_str}\n---")
    if text := (
        process_file_based_on_type(source_str, clean, verbose)
        if is_local_file(source_str)
        else process_remote_file_based_on_type(source_str, clean, verbose)
    ):
        print(text)
    elif verbose:
        print(f"No text found or unsupported source for {source_str}.")


def process_file_based_on_type(
    file_path: str, clean: bool = True, content: str | None = None, verbose: bool = False
) -> str | None:
    """Process a file based on its type, content can be passed directly if already fetched."""
    file_type = get_file_type_from_file(file_path, verbose)
    if file_type == "text":
        return pathlib.Path(file_path).read_text()
    elif file_type == "html":
        html = pathlib.Path(file_path).read_text()
        return clean_html(html, verbose) if clean else html
    elif file_type == "pdf":
        return process_pdf_file(file_path, verbose)


def process_remote_file_based_on_type(url: str, clean: bool = True, verbose: bool = False) -> str | bytes | None:
    """Process a remote file based on its type."""
    content = get_url(url)
    file_type = get_file_type_from_buffer(content, verbose)
    if file_type == "text":
        return content
    elif file_type == "html":
        return clean_html(content, verbose) if clean else content
    elif file_type == "pdf":
        binary_content = get_url(url, binary=True, verbose=verbose)
        return process_pdf_content(binary_content, verbose)


def get_file_type_from_file(path, verbose: bool = False):
    """Determine the MIME type of a file and return its general type if recognized."""
    mime_type = magic.from_file(path, mime=True)
    # Handle empty files
    if "html" in mime_type:
        return "html"
    elif "pdf" in mime_type:
        return "pdf"
    elif "text" in mime_type:
        return "text"
    elif verbose:
        print(f"Unsupported file type: {mime_type}")


def get_file_type_from_buffer(buffer, verbose: bool = False):
    """Determine the MIME type from a memory buffer and return its general type if recognized."""
    mime_type = magic.from_buffer(buffer, mime=True)
    if "html" in mime_type:
        return "html"
    elif "text" in mime_type:
        return "text"
    elif "pdf" in mime_type:
        return "pdf"
    elif verbose:
        print(f"Unsupported file type: {mime_type}")


def get_url(url: str, binary: bool = False, verbose: bool = False) -> str | bytes:
    """Download webpage and return the content as text or binary."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.content if binary else response.text
    except requests.RequestException as e:
        raise typer.Exit(f"Error downloading {url}: {e}") from e


def clean_html(html: str, verbose: bool = False) -> str:
    """Clean the HTML using Document and BeautifulSoup."""
    doc = Document(html)
    summary_html = doc.summary()
    soup = BeautifulSoup(summary_html, "html.parser")
    return soup.get_text()


def process_pdf_content(pdf_content: bytes, verbose: bool = False) -> str | None:
    """Extract text from a PDF content using PyMuPDF."""
    try:
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception as e:
        if verbose:
            print(f"Error processing PDF content: {e}")
        return None


def process_pdf_file(file_path: str, verbose: bool = False) -> str | None:
    """Extract text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception as e:
        if verbose:
            print(f"Error processing PDF content: {e}")
        return None


def is_local_file(path: str, verbose: bool = False) -> bool:
    """Check if the given path is a local file, a URL, or neither, and raise an error if it's neither."""

    # Check if the path is a URL by looking for URL schemes
    if re.match(r"https?://", path):
        return False
    # Check if the path exists and is a file or a directory
    if pathlib.Path(path).is_file() or pathlib.Path(path).is_dir():
        return True
    # Raise an error if the path is neither a valid URL nor a local file or directory
    raise ValueError(f"Invalid path: {path} is neither a valid URL nor a local file or directory.")


if __name__ == "__main__":
    app()
