import json
import os
from pathlib import Path
from typing import Dict, Optional, Union

from bson import ObjectId

from retk import const, utils
from retk._version import __version__


def dump_dot_rethink(path: Union[os.PathLike, Path]) -> Dict:
    version = {
        "version": __version__,
        "_id": ObjectId(),
        "id": utils.short_uuid(),
        "email": const.DEFAULT_USER["email"],
        "nickname": const.DEFAULT_USER["nickname"],
        "avatar": const.DEFAULT_USER["avatar"],
        "account": const.DEFAULT_USER["email"],
        "settings": {
            "language": os.getenv("VUE_APP_LANGUAGE", const.Language.EN.value),
            "theme": const.AppTheme.LIGHT.value,
            "editorMode": const.EditorMode.WYSIWYG.value,
            "editorFontSize": 15,
            "editorCodeTheme": const.EditorCodeTheme.GITHUB.value,
            "editorSepRightWidth": 200,
            "editorSideCurrentToolId": "",
        }
    }
    with open(path, "w", encoding="utf-8") as f:
        out = version.copy()
        out["_id"] = str(out["_id"])
        json.dump(out, f, indent=2, ensure_ascii=False)
    return version


def load_dot_rethink(path: Union[os.PathLike, Path]) -> Optional[Dict]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
