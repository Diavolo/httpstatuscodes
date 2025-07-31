import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional

from markdown import markdown
import yaml

from app.utils.constants import (
    CODES_DIR_NAME,
    CONTENT_DIR_PATH,
    DEFAULT_LANGUAGE,
    MD_HEADER_META_REGEX,
    SUPPORTED_LANGUAGES,
)
from app.utils.files import (
    get_error_content,
    read_file_content,
    read_http_status_files,
)
from app.utils.html import strip_tags
from app.utils.md import MD_EXTENSIONS, MD_EXTENSION_CONFIGS

logger = logging.getLogger(__name__)


class ContentService:
    """Service for handling content operations and business logic."""

    @staticmethod
    def get_content_path(
        lang: str, content_type: str, filename: Optional[str] = None
    ) -> Path:
        """Get the content path in the correct language.

        Args:
            lang (str): The language.
            content_type (str): The content type.
            filename (str, optional): The filename. Defaults to None.

        Returns:
            Path: The content path.
        """
        if lang not in SUPPORTED_LANGUAGES:
            lang = DEFAULT_LANGUAGE

        if content_type == "codes":
            return (
                CONTENT_DIR_PATH.joinpath(lang)
                .joinpath(CODES_DIR_NAME)
                .joinpath(f"{filename}.md")
            )
        else:
            return CONTENT_DIR_PATH.joinpath(lang).joinpath(f"{filename}.md")

    @staticmethod
    def get_page_content(lang: str, page_name: str) -> Dict[str, Any]:
        """Get page content for a specific language and page.

        Args:
            lang (str): The language.
            page_name (str): The page name (index, about, contact).

        Returns:
            Dict[str, Any]: Dictionary containing headline and context data.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            content_path = ContentService.get_content_path(lang, "page", page_name)

            with open(content_path, "r", encoding="utf-8") as page_file:
                page_md_content = page_file.read()
                headline = markdown(
                    page_md_content.split("---")[2],
                    extension_configs=MD_EXTENSION_CONFIGS,
                )

            http_codes_categories = read_http_status_files(lang)

            return {
                "headline": headline,
                "http_codes_collection": http_codes_categories,
                "current_lang": lang,
                "default_lang": DEFAULT_LANGUAGE,
                "supported_languages": SUPPORTED_LANGUAGES,
            }

        except IOError as e:
            logger.error(f"Error reading {page_name} page for language: {lang}")
            raise e

    @staticmethod
    def get_code_content(lang: str, code: int) -> Dict[str, Any]:
        """Get HTTP status code content for a specific language and code.

        Args:
            lang (str): The language.
            code (int): The HTTP status code.

        Returns:
            Dict[str, Any]: Dictionary containing code content and metadata.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            code_md_file_path = ContentService.get_content_path(lang, "codes", code)
            code_md_content = read_file_content(code_md_file_path)

        except IOError as e:
            logger.error(f"Error reading code {code} for language: {lang}")
            raise e

        http_codes_categories = read_http_status_files(lang)
        md_content_divided = code_md_content.split("---")

        content_meta = yaml.safe_load(md_content_divided[1])
        content_body = markdown(
            md_content_divided[2],
            extensions=[*MD_EXTENSIONS],
            extension_configs=MD_EXTENSION_CONFIGS,
        )
        content_footnotes = markdown(
            md_content_divided[3],
            extensions=[*MD_EXTENSIONS],
            extension_configs=MD_EXTENSION_CONFIGS,
        )

        content = markdown(
            re.sub(MD_HEADER_META_REGEX, "", code_md_content),
            extensions=[*MD_EXTENSIONS],
            extension_configs=MD_EXTENSION_CONFIGS,
        )

        page_description = strip_tags(content_body.split("\n")[0])

        return {
            "page_description": page_description,
            "content_meta": content_meta,
            "content_body": content_body,
            "content_footnotes": content_footnotes,
            "content": content,
            "http_codes_collection": http_codes_categories,
            "current_lang": lang,
            "default_lang": DEFAULT_LANGUAGE,
            "supported_languages": SUPPORTED_LANGUAGES,
        }

    @staticmethod
    def get_license_content() -> Dict[str, str]:
        """Get license content.

        Returns:
            Dict[str, str]: Dictionary containing license content.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open("LICENSE", "r", encoding="utf-8") as license_file:
                license_content = license_file.read()
                # Remove lines starting with "Copyright (c)" to prevent spam
                lines = license_content.split("\n")
                filtered_lines = [
                    line
                    for line in lines
                    if not line.strip().startswith("Copyright (c)")
                ]
                license_content = "\n".join(filtered_lines)

            return {"headline": license_content}

        except IOError as e:
            logger.error("Error reading LICENSE file")
            raise e

    @staticmethod
    def get_error_content(error_type: str) -> Dict[str, str]:
        """Get error content.

        Args:
            error_type (str): The error type.

        Returns:
            Dict[str, str]: Dictionary containing error content.
        """
        headline = get_error_content(error_type)
        if headline == "":
            raise IOError(f"Error reading {error_type} file")
        return {"headline": headline}
