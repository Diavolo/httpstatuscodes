from os.path import exists
import json
import re

from flask import Blueprint, render_template, request, send_from_directory
from markdown import markdown
import yaml

from app.utils.constants import (
    CODE_NOT_FOUND_MSG, CODES_DIR_PATH, CONTENTS_DIR_PATH, DIR_NOT_FOUND_MSG,
    FILE_ERROR_READING_MSG, MD_HEADER_META_REGEX)
from app.utils.html import strip_tags
from app.utils.md import MD_EXTENSIONS, MD_EXTENSION_CONFIGS

home = Blueprint("home", __name__)


@home.route("/")
def index():
    if not exists(CODES_DIR_PATH):
        return render_template("404.html", error_message=DIR_NOT_FOUND_MSG), 404

    try:
        with CODES_DIR_PATH.joinpath("classes.json").open() as classes_from_json:
            http_codes_collection = json.load(classes_from_json)
    except IOError:
        return render_template("404.html", error_message=FILE_ERROR_READING_MSG.format("JSON")), 404

    try:
        with open(CONTENTS_DIR_PATH.joinpath("index.md"), "r", encoding="utf-8") as index_file:
            index_md_content = index_file.read()
            headline = markdown(index_md_content.split("---")[2],
                                extension_configs=MD_EXTENSION_CONFIGS)
    except IOError:
        return render_template("404.html", error_message=FILE_ERROR_READING_MSG.format("MD"))

    for item in CODES_DIR_PATH.glob("*.md"):
        if item.is_file():
            try:
                with open(item, "r", encoding="utf-8") as md_file:
                    md_file_content = md_file.read()

                md_content_divided = md_file_content.split("---")

                file_content_meta = yaml.safe_load(md_content_divided[1])

                code = {
                    "code": file_content_meta["code"],
                    "set": file_content_meta["set"],
                    "title": file_content_meta["title"]
                }

                if str(code["set"]) in http_codes_collection.keys():
                    if "codes" in http_codes_collection[str(code["set"])]:
                        http_codes_collection[str(
                            code["set"])]["codes"].append(code)
                        http_codes_collection[str(code["set"])]["codes"] = sorted(
                            http_codes_collection[str(
                                code["set"])]["codes"], key=lambda item: item.get("code")
                        )
                    else:
                        http_codes_collection[str(code["set"])]["codes"] = [
                            code]
            except:
                continue

    context = {
        "headline": headline,
        "http_codes_collection": http_codes_collection
    }

    return render_template("index.html", **context)


@home.route("/about/")
def about():
    return render_template("about.html")


@home.route("/contact/")
def contact():
    return render_template("contact.html")


@home.route("/humans.txt")
def humans():
    return send_from_directory(CONTENTS_DIR_PATH, request.path[1:])


@home.route("/<int:code>/")
def get_code(code: int):
    if not exists(CODES_DIR_PATH):
        return render_template("404.html", error_message=DIR_NOT_FOUND_MSG), 404

    code_md_file_path = CODES_DIR_PATH.joinpath(f"{code}.md")

    if not code_md_file_path.is_file():
        return render_template("404.html", error_message=CODE_NOT_FOUND_MSG), 404

    try:
        with open(code_md_file_path, "r", encoding="utf-8") as code_md_file:
            code_md_content = code_md_file.read()
    except IOError:
        return render_template("404.html", error_message=FILE_ERROR_READING_MSG.format("MD")), 404

    md_content_divided = code_md_content.split("---")

    content_meta = yaml.safe_load(md_content_divided[1])
    content_body = markdown(md_content_divided[2],
                            extensions=[*MD_EXTENSIONS],
                            extension_configs=MD_EXTENSION_CONFIGS)
    content_footnotes = markdown(md_content_divided[3],
                                 extensions=[*MD_EXTENSIONS],
                                 extension_configs=MD_EXTENSION_CONFIGS)

    content = markdown(re.sub(MD_HEADER_META_REGEX, '', code_md_content),
                       extensions=[*MD_EXTENSIONS],
                       extension_configs=MD_EXTENSION_CONFIGS)

    page_description = strip_tags(content_body.split("\n")[0])

    try:
        with CODES_DIR_PATH.joinpath("classes.json").open() as classes_from_json:
            http_codes_collection = json.load(classes_from_json)
    except IOError:
        return render_template("404.html", error_message=FILE_ERROR_READING_MSG.format("JSON")), 404

    context = {
        "page_description": page_description,
        "content_meta": content_meta,
        "content_body": content_body,
        "content_footnotes": content_footnotes,
        "content": content,
        "http_codes_collection": http_codes_collection
    }
    return render_template("code.html", **context)
