from genericpath import exists
import json

from flask import Blueprint, jsonify, request, url_for
from markdown import markdown
import yaml

from app.utils.constants import (
    CODE_NOT_FOUND_MSG, CODES_DIR_PATH, DIR_NOT_FOUND_MSG,
    FILE_ERROR_READING_MSG)
from app.utils.html import strip_tags


api = Blueprint("api", __name__, url_prefix='/api')


@api.route("/<int:code>/")
def get_api_code(code: int):
    if not exists(CODES_DIR_PATH):
        return {"message": DIR_NOT_FOUND_MSG}, 404

    md_file_path = CODES_DIR_PATH.joinpath(f"{code}.md")

    if not md_file_path.is_file():
        return {"message": CODE_NOT_FOUND_MSG}, 404

    try:
        with open(md_file_path, "r", encoding="utf-8") as md_file:
            text = md_file.read()
    except IOError:
        return {"message": FILE_ERROR_READING_MSG.format("MD")}, 500

    content_divided = text.split("---")
    content_meta = yaml.safe_load(content_divided[1])
    content_body = markdown(content_divided[2])

    try:
        with CODES_DIR_PATH.joinpath("classes.json").open() as classes_from_json:
            http_codes_categories = json.load(classes_from_json)
    except IOError:
        return {"message": FILE_ERROR_READING_MSG.format("JSON")}, 500

    category_title = str(
        http_codes_categories[str(content_meta["set"])]["title"])

    location = request.host_url[:-1] + url_for("home.get_code", code=code)

    json_resp = {
        "location": location,
        "status_code": content_meta["code"],
        "category": category_title.replace("&times;&times; ", "-").split("-")[1],
        "title": content_meta["title"],
        "description": strip_tags(content_body.split("\n")[0])
    }
    return jsonify(json_resp), 200
