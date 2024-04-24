import pytest
from makefile_to_markdown.core import extract_command
from makefile_to_markdown.core import extract_headers
from makefile_to_markdown.core import makefile_2_markdown
from makefile_to_markdown.core import read_lines
from makefile_to_markdown.core import save_content
from makefile_to_markdown.core import start_new_table


@pytest.fixture()
def makefile_content():
    return (
        "# ----\n# Generate help output when running just `make`\n# ----\n"
        "# ----\n# Variables\n# ----\n"
        "# ----\n# Header1\n# ----\n"
        "test-command: ## This is a test command\n"
        "# ----\n# Header2\n# ----\n"
        "foo-command: ## This is a foo command\n"
    )


def test_read_lines(tmp_path):
    p = tmp_path / "test.txt"
    p.write_text("line1\nline2\nline3")
    lines = read_lines(p)
    assert lines == ["line1", "line2", "line3"]


def test_save_content(tmp_path):
    p = tmp_path / "test.txt"
    save_content(p, "test content")
    content = p.read_text()
    assert content == "test content"


def test_extract_headers(tmp_path, makefile_content):
    p = tmp_path / "test.txt"
    p.write_text(makefile_content)
    headers = extract_headers(p)
    assert headers == ["Header1", "Header2"]


def test_start_new_table():
    table = start_new_table()
    assert table == "| Command | Description |\n| --- | --- |\n"


def test_extract_command():
    line = "test-command: ## This is a test command"
    command, description = extract_command(line)
    assert command == "test-command"
    assert description == "This is a test command"


def test_extract_command_no_description():
    line = "test-command:"
    command, description = extract_command(line)
    assert command is None
    assert description is None


def test_makefile_2_markdown(tmp_path, makefile_content):
    makefile = tmp_path / "Makefile"
    makefile.write_text(makefile_content)
    output = tmp_path / "output.md"
    makefile_2_markdown(makefile, output)
    content = output.read_text()
    assert "## Makefile Commands" in content
    assert "# Header1" in content
    assert "| Command | Description |\n| --- | --- |\n" in content
    assert "| `test-command` | This is a test command |" in content


def test_makefile_2_markdown_no_output(tmp_path, makefile_content):
    makefile = tmp_path / "Makefile"
    makefile.write_text(makefile_content)
    makefile_2_markdown(makefile)
    output = tmp_path / "Makefile-commands.md"
    content = output.read_text()
    assert "## Makefile Commands" in content
    assert "# Header1" in content
    assert "| Command | Description |\n| --- | --- |\n" in content
    assert "| `test-command` | This is a test command |" in content
