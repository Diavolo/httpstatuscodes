from pathlib import Path


APP_DIR_PATH = Path(__file__).resolve().parent.parent
CONTENTS_DIR_PATH = APP_DIR_PATH.joinpath("contents")
CODES_DIR_PATH = CONTENTS_DIR_PATH.joinpath("codes")

DIR_NOT_FOUND_MSG = "Directory not found."
CODE_NOT_FOUND_MSG = "HTTP Status Code not found."
FILE_ERROR_READING_MSG = "Error reading {} file."

MD_HEADER_META_REGEX = "^-{3}(\n#.*)*(\n.*:.*)+(\n#.*)*\n-{3}"

HTTP_STATUS_CODES_CATEGORIES: dict[str, dict[str:str]] = {
    "1": {
        "title": "1&times;&times; Informational",
        "icon": "info",
        "color": "blue",
        "class": "informational",
        "emoji": "🔵",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M12 1C5.925 1 1 5.925 1 12s4.925 11 11 11s11-4.925 11-11S18.075 1 12 1m-.5 5a1 1 0 1 0 0 2h.5a1 1 0 1 0 0-2zM10 10a1 1 0 1 0 0 2h1v3h-1a1 1 0 1 0 0 2h4a1 1 0 1 0 0-2h-1v-4a1 1 0 0 0-1-1z" clip-rule="evenodd"/></svg>',
        "description": "Indicates an interim response for communicating connection status or request progress prior to completing the requested action and sending a final response.",
    },
    "2": {
        "title": "2&times;&times; Success",
        "icon": "check",
        "color": "green",
        "class": "success",
        "emoji": "✅",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M12 1C5.925 1 1 5.925 1 12s4.925 11 11 11s11-4.925 11-11S18.075 1 12 1m4.768 9.14a1 1 0 1 0-1.536-1.28l-4.3 5.159l-2.225-2.226a1 1 0 0 0-1.414 1.414l3 3a1 1 0 0 0 1.475-.067z" clip-rule="evenodd"/></svg>',
        "description": "Indicates that the client's request was successfully received, understood, and accepted.",
    },
    "3": {
        "title": "3&times;&times; Redirection",
        "icon": "arrow-right",
        "color": "yellow",
        "class": "redirection",
        "emoji": "➡️",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 16 16"><path fill="currentColor" d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0M4.5 7.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"/></svg>',
        "description": "Indicates that further action needs to be taken by the user agent in order to fulfill the request.",
    },
    "4": {
        "title": "4&times;&times; Client Error",
        "icon": "exclamation-triangle",
        "color": "orange",
        "class": "client-error",
        "emoji": "🟠",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 2C6.579 2 2 6.579 2 12s4.579 10 10 10s10-4.579 10-10S17.421 2 12 2zm0 5c1.727 0 3 1.272 3 3s-1.273 3-3 3c-1.726 0-3-1.272-3-3s1.274-3 3-3zm-5.106 9.772c.897-1.32 2.393-2.2 4.106-2.2h2c1.714 0 3.209.88 4.106 2.2C15.828 18.14 14.015 19 12 19s-3.828-.86-5.106-2.228z" fill="currentColor"/></svg>',
        "description": "Indicates that the client seems to have erred in the request.",
    },
    "5": {
        "title": "5&times;&times; Server Error",
        "icon": "server",
        "color": "red",
        "class": "server-error",
        "emoji": "🔥",
        "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 16 16"><path fill="currentColor" d="M8 16c3.314 0 6-2 6-5.5c0-1.5-.5-4-2.5-6c.25 1.5-1.25 2-1.25 2C11 4 9 .5 6 0c.357 2 .5 4-2 6c-1.25 1-2 2.729-2 4.5C2 14 4.686 16 8 16m0-1c-1.657 0-3-1-3-2.75c0-.75.25-2 1.25-3C6.125 10 7 10.5 7 10.5c-.375-1.25.5-3.25 2-3.5c-.179 1-.25 2 1 3c.625.5 1 1.364 1 2.25C11 14 9.657 15 8 15"/></svg>',
        "description": "Indicates that the server is aware that it has erred or is incapable of performing the requested method.",
    },
}
