from os.path import exists
from pathlib import Path
import logging

from markdown import markdown
import yaml

from app.utils.constants import (
    CODE_NOT_FOUND_MSG,
    CODES_DIR_NAME,
    CONTENT_DIR_PATH,
    DEFAULT_LANGUAGE,
    DIR_NOT_FOUND_MSG,
    FILE_ERROR_READING_MSG,
    HTTP_STATUS_CODES_CATEGORIES,
    SUPPORTED_LANGUAGES,
)
from app.utils.md import MD_EXTENSION_CONFIGS

logger = logging.getLogger(__name__)


def get_error_content(error_type: str) -> str:
    """Get the content of an error file (e.g. error-404.md).

    Args:
        error_type (str): The error type.

    Returns:
        str: The content if it exists, otherwise an empty string.
    """
    try:
        with open(
            CONTENT_DIR_PATH.joinpath(f"error-{error_type}.md"), "r", encoding="utf-8"
        ) as error_md_file:
            error_md_content = error_md_file.read()
            headline = markdown(
                error_md_content.split("---")[2],
                extension_configs=MD_EXTENSION_CONFIGS,
            )

        return headline
    except IOError:
        return ""


def validate_content_directory(content_directory: str) -> None:
    """Validate the content directory.

    Args:
        content_directory (str): The content directory.

    Raises:
        IOError: If the content directory does not exist.
    """
    if not exists(content_directory):
        raise IOError(DIR_NOT_FOUND_MSG)


def validate_file_path(file_path: Path) -> None:
    """Validate the file path.

    Args:
        file_path (Path): The file path.

    Raises:
        IOError: If the file path does not exist.
    """
    if not file_path.is_file():
        error_content = get_error_content("404")
        print(len(error_content))
        error_content = error_content if error_content != "" else CODE_NOT_FOUND_MSG
        raise IOError(error_content)


def read_file_content(file_path: Path) -> str:
    """Read the content of a file.

    Args:
        file_path (Path): The file path.

    Raises:
        IOError: If the file does not exist.

    Returns:
        str: The file content.
    """

    validate_file_path(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        raise IOError(f"{FILE_ERROR_READING_MSG.format('MD')}: {str(e)}")


def read_http_status_files(lang: str = DEFAULT_LANGUAGE) -> dict[str, dict]:
    """Read the HTTP status files.

    Args:
        lang (str, optional): The language. Defaults to DEFAULT_LANGUAGE.

    Returns:
        dict[str, dict]: The HTTP status categories.
    """
    http_codes_categories = {
        k: v.copy() for k, v in HTTP_STATUS_CODES_CATEGORIES.items()
    }

    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    codes_dir_path = CONTENT_DIR_PATH.joinpath(lang).joinpath(CODES_DIR_NAME)

    for item in codes_dir_path.glob("*.md"):
        if item.is_file():
            try:
                with open(item, "r", encoding="utf-8") as md_file:
                    md_file_content = md_file.read()

                md_content_divided = md_file_content.split("---")

                file_content_meta = yaml.safe_load(md_content_divided[1])

                code = {
                    "set": file_content_meta["set"],
                    "code": file_content_meta["code"],
                    "title": file_content_meta["title"],
                }

                markdown_header_set_value = str(code["set"])

                if markdown_header_set_value not in http_codes_categories.keys():
                    continue

                if "codes" in http_codes_categories[markdown_header_set_value]:
                    http_codes_categories[markdown_header_set_value]["codes"].append(
                        code
                    )
                    http_codes_categories[markdown_header_set_value]["codes"] = sorted(
                        http_codes_categories[markdown_header_set_value]["codes"],
                        key=lambda item: item.get("code"),
                    )
                else:
                    http_codes_categories[markdown_header_set_value]["codes"] = [code]
            except:
                logger.error(f"Error reading {item} file.")
                continue

    return http_codes_categories
