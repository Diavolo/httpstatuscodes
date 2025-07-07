from os.path import exists
from pathlib import Path

from markdown import markdown
import yaml

from app.utils.constants import (
    CODE_NOT_FOUND_MSG,
    CODES_DIR_PATH,
    CONTENTS_DIR_PATH,
    DIR_NOT_FOUND_MSG,
    FILE_ERROR_READING_MSG,
    HTTP_STATUS_CODES_CATEGORIES,
)
from app.utils.md import MD_EXTENSION_CONFIGS


def get_page_404_content() -> str:
    try:
        with open(
            CONTENTS_DIR_PATH.joinpath("error-404.md"), "r", encoding="utf-8"
        ) as not_found_md_file:
            not_found_md_content = not_found_md_file.read()
            headline = markdown(
                not_found_md_content.split("---")[2],
                extension_configs=MD_EXTENSION_CONFIGS,
            )

        return headline
    except IOError:
        return ""


def get_page_500_content() -> str:
    try:
        with open(
            CONTENTS_DIR_PATH.joinpath("error-500.md"), "r", encoding="utf-8"
        ) as internal_server_error_md_file:
            internal_server_error_md_content = internal_server_error_md_file.read()
            headline = markdown(
                internal_server_error_md_content.split("---")[2],
                extension_configs=MD_EXTENSION_CONFIGS,
            )

        return headline
    except IOError:
        return ""


def validate_content_directory(content_directory: str) -> None:
    if not exists(content_directory):
        raise IOError(DIR_NOT_FOUND_MSG)


def validate_file_path(file_path: Path) -> None:
    if not file_path.is_file():
        error_content = get_page_404_content()
        print(len(error_content))
        error_content = error_content if error_content != "" else CODE_NOT_FOUND_MSG
        raise IOError(error_content)


def read_file_content(file_path: Path) -> str:
    """Read the content of a file."""

    validate_file_path(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except IOError as e:
        raise IOError(f"{FILE_ERROR_READING_MSG.format('MD')}: {str(e)}")


def read_http_status_files() -> dict[str, dict]:
    http_codes_categories = {
        k: v.copy() for k, v in HTTP_STATUS_CODES_CATEGORIES.items()
    }

    for item in CODES_DIR_PATH.glob("*.md"):
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
                continue

    return http_codes_categories
