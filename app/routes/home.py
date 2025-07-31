from http import HTTPStatus
from pathlib import Path
import re

from flask import Blueprint, redirect, render_template, request, send_from_directory
from markdown import markdown
import yaml

from app.utils.constants import (
    CODES_DIR_NAME,
    CODES_DIR_PATH,
    CONTENTS_DIR_PATH,
    DEFAULT_LANGUAGE,
    FILE_ERROR_READING_MSG,
    HTTP_STATUS_CODES_CATEGORIES,
    MD_HEADER_META_REGEX,
    NOT_FOUND_HTML_TEMPLATE,
    SUPPORTED_LANGUAGES,
)
from app.utils.files import (
    get_page_404_content,
    read_file_content,
    read_http_status_files,
)
from app.utils.html import strip_tags
from app.utils.md import MD_EXTENSIONS, MD_EXTENSION_CONFIGS

home = Blueprint("home", __name__)


def get_language_from_path() -> str:
    """Get the language from the path.

    Returns:
        str: The language from the path.
    """
    path_parts = request.path.strip("/").split("/")
    if path_parts and path_parts[0] in SUPPORTED_LANGUAGES:
        return path_parts[0]
    return DEFAULT_LANGUAGE


def get_content_path(lang, content_type, filename=None):
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
        return CONTENTS_DIR_PATH.joinpath(lang).joinpath(CODES_DIR_NAME).joinpath(f"{filename}.md")
    else:
        return CONTENTS_DIR_PATH.joinpath(lang).joinpath(f"{filename}.md")


def get_available_translations(code: str):
    """Get the available translations for a given code.

    Args:
        code (str): The code.

    Returns:
        dict: The available translations.
    """
    translations: dict[str, str] = {}
    for lang in SUPPORTED_LANGUAGES:
        code_path = get_content_path(lang, "codes", code)
        if code_path.exists():
            translations[lang] = code_path
    return translations


@home.route("/")
def index_redirect():
    accept_language = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
    if accept_language and accept_language != DEFAULT_LANGUAGE:
        return redirect(f"/{accept_language}/")
    return redirect("/en/")


@home.route("/<lang>/")
def index(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect("/en/")

    try:
        content_path = get_content_path(lang, "page", "index")

        with open(content_path, "r", encoding="utf-8") as index_file:
            index_md_content = index_file.read()
            headline = markdown(
                index_md_content.split("---")[2], extension_configs=MD_EXTENSION_CONFIGS
            )
    except IOError:
        if lang != DEFAULT_LANGUAGE:
            return redirect("/en/")
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )

    """
    http_codes_categories = {
        k: v.copy() for k, v in HTTP_STATUS_CODES_CATEGORIES.items()
    }

    try:
        with open(
            CONTENTS_DIR_PATH.joinpath("index.md"), "r", encoding="utf-8"
        ) as index_file:
            index_md_content = index_file.read()
            headline = markdown(
                index_md_content.split("---")[2], extension_configs=MD_EXTENSION_CONFIGS
            )
    except IOError:
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )
    """

    http_codes_categories = read_http_status_files(lang)

    context = {
        "headline": headline,
        "http_codes_collection": http_codes_categories,
        "current_lang": lang,
        "supported_languages": SUPPORTED_LANGUAGES,
    }

    return render_template("index.html", **context)


@home.route("/about/")
def about():
    try:
        with open(
            CONTENTS_DIR_PATH.joinpath(DEFAULT_LANGUAGE).joinpath("about.md"), "r", encoding="utf-8"
        ) as about_file:
            about_md_content = about_file.read()
            headline = markdown(
                about_md_content.split("---")[2], extension_configs=MD_EXTENSION_CONFIGS
            )
        context = {"headline": headline}

        return render_template("about.html", **context)
    except IOError:
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/contact/")
def contact():
    try:
        with open(
            CONTENTS_DIR_PATH.joinpath(DEFAULT_LANGUAGE).joinpath("contact.md"), "r", encoding="utf-8"
        ) as contact_file:
            contact_md_content = contact_file.read()
            headline = markdown(
                contact_md_content.split("---")[2],
                extension_configs=MD_EXTENSION_CONFIGS,
            )
        context = {"headline": headline}

        return render_template("contact.html", **context)
    except IOError:
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/license/")
def license():
    try:
        with open("LICENSE", "r", encoding="utf-8") as license_file:
            license_content = license_file.read()
            # Remove lines starting with "Copyright (c)" to prevent spam
            lines = license_content.split("\n")
            filtered_lines = [
                line for line in lines if not line.strip().startswith("Copyright (c)")
            ]
            license_content = "\n".join(filtered_lines)
            headline = license_content
        context = {"headline": headline}

        return render_template("license.html", **context)
    except IOError:
        return render_template(
            NOT_FOUND_HTML_TEMPLATE,
            error_message=FILE_ERROR_READING_MSG.format("LICENSE"),
        )


@home.route("/humans.txt")
def humans():
    return send_from_directory(CONTENTS_DIR_PATH, request.path[1:])


@home.route("/<lang>/<int:code>/")
def get_code(lang: str, code: int):
    if lang not in SUPPORTED_LANGUAGES:
        return redirect(f"/en/{code}/")

    try:
        #code_md_file_path = CODES_DIR_PATH.joinpath(f"{code}.md")
        code_md_file_path = get_content_path(lang, "codes", code)
        code_md_content = read_file_content(code_md_file_path)
    except IOError as e:
        if lang != DEFAULT_LANGUAGE:
            return redirect(f"/en/{code}/")
        error_content = get_page_404_content()
        error_content = error_content if error_content != "" else str(e)
        context = {
            "error_message": error_content,
        }
        return render_template(NOT_FOUND_HTML_TEMPLATE, **context), HTTPStatus.NOT_FOUND

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

    context = {
        "page_description": page_description,
        "content_meta": content_meta,
        "content_body": content_body,
        "content_footnotes": content_footnotes,
        "content": content,
        "http_codes_collection": http_codes_categories,
        "current_lang": lang,
        "supported_languages": SUPPORTED_LANGUAGES,
    }
    return render_template("code.html", **context)


@home.route("/<int:code>/")
def get_code_redirect(code: int):
    return redirect(f"/en/{code}/")
