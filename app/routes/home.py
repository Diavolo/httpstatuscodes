from http import HTTPStatus
import logging

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from app.services.content_service import ContentService
from app.utils.constants import (
    CONTENT_DIR_PATH,
    DEFAULT_LANGUAGE,
    FILE_ERROR_READING_MSG,
    NOT_FOUND_HTML_TEMPLATE,
    SUPPORTED_LANGUAGES,
)

logger = logging.getLogger(__name__)

home = Blueprint("home", __name__)


@home.route("/")
def index():
    lang = DEFAULT_LANGUAGE

    try:
        context = ContentService.get_page_content(lang, "index")
        return render_template("index.html", **context)
    except IOError:
        logger.error(f"Error reading index page for language: {lang}")
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/<lang>/")
def index_i18n(lang: str):
    accept_language = request.accept_languages.best_match(SUPPORTED_LANGUAGES)
    if accept_language and accept_language != DEFAULT_LANGUAGE:
        lang = accept_language

    if lang not in SUPPORTED_LANGUAGES or lang == DEFAULT_LANGUAGE:
        return redirect(url_for("home.index"))

    try:
        context = ContentService.get_page_content(lang, "index")
        return render_template("index.html", **context)
    except IOError:
        logger.error(f"Error reading index page for language: {lang}")
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/about/")
def about():
    lang = DEFAULT_LANGUAGE

    try:
        context = ContentService.get_page_content(lang, "about")
        return render_template("about.html", **context)
    except IOError:
        logger.error(f"Error reading about page for language: {lang}")
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/<lang>/about/")
def about_i18n(lang: str):
    if lang not in SUPPORTED_LANGUAGES or lang == DEFAULT_LANGUAGE:
        return redirect(url_for("home.about"))

    try:
        context = ContentService.get_page_content(lang, "about")
        return render_template("about.html", **context)
    except IOError:
        logger.error(f"Error reading about page for language: {lang}")
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/contact/")
def contact():
    lang = DEFAULT_LANGUAGE

    try:
        context = ContentService.get_page_content(lang, "contact")
        return render_template("contact.html", **context)
    except IOError:
        logger.error(f"Error reading contact page for language: {lang}")
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/<lang>/contact/")
def contact_i18n(lang: str):
    if lang not in SUPPORTED_LANGUAGES or lang == DEFAULT_LANGUAGE:
        return redirect(url_for("home.contact"))

    try:
        context = ContentService.get_page_content(lang, "contact")
        return render_template("contact.html", **context)
    except IOError:
        logger.error(f"Error reading contact page for language: {lang}")
        return render_template(
            NOT_FOUND_HTML_TEMPLATE, error_message=FILE_ERROR_READING_MSG.format("MD")
        )


@home.route("/license/")
def license():
    try:
        context = ContentService.get_license_content()
        return render_template("license.html", **context)
    except IOError:
        return render_template(
            NOT_FOUND_HTML_TEMPLATE,
            error_message=FILE_ERROR_READING_MSG.format("LICENSE"),
        )


@home.route("/<lang>/license/")
def license_redirect(lang: str):
    logger.info(f"Redirecting to license page for language: {lang}")
    return redirect(url_for("home.license"))


@home.route("/humans.txt")
def humans():
    return send_from_directory(CONTENT_DIR_PATH, request.path[1:])


@home.route("/<int:code>/")
def get_code(code: int):
    lang = DEFAULT_LANGUAGE

    try:
        context = ContentService.get_code_content(lang, code)
        return render_template("code.html", **context)
    except IOError as e:
        error_content = ContentService.get_error_content("404")
        error_content = error_content if error_content != "" else str(e)
        context = {"error_message": error_content}
        return render_template(NOT_FOUND_HTML_TEMPLATE, **context), HTTPStatus.NOT_FOUND


@home.route("/<lang>/<int:code>/")
def get_code_i18n(lang: str, code: int):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    if lang == DEFAULT_LANGUAGE:
        return redirect(url_for("home.get_code"))

    try:
        context = ContentService.get_code_content(lang, code)
        return render_template("code.html", **context)
    except IOError as e:
        if lang != DEFAULT_LANGUAGE:
            return redirect(f"/en/{code}/")
        error_content = ContentService.get_error_content("404")
        error_content = error_content if error_content != "" else str(e)
        context = {"error_message": error_content}
        return render_template(NOT_FOUND_HTML_TEMPLATE, **context), HTTPStatus.NOT_FOUND
