from typing import Any, Optional, TypedDict

from .variableAndKeyString import variableAndKeyString

space = ' - '


def debugObj(obj: dict[str, Any], keys: list[str] | None = None):
    if not keys:
        keys = list(filter(lambda key: not key.startswith('__'), obj.keys()))
    res = '\n'.join(
        list(
            filter(
                None,
                map(
                    lambda a: variableAndKeyString(obj, a),
                    keys,
                ),
            )
        )
    )
    res = space + res.strip().replace('\n', '\n' + space)
    return res
