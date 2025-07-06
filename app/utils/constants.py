from pathlib import Path


APP_DIR_PATH = Path(__file__).resolve().parent.parent
CONTENTS_DIR_PATH = APP_DIR_PATH.joinpath("contents")
CODES_DIR_PATH = CONTENTS_DIR_PATH.joinpath("codes")

DIR_NOT_FOUND_MSG = "Directory not found."
CODE_NOT_FOUND_MSG = "HTTP Status Code not found."
FILE_ERROR_READING_MSG = "Error reading {} file."

MD_HEADER_META_REGEX = '^-{3}(\n#.*)*(\n.*:.*)+(\n#.*)*\n-{3}'
