from __future__ import annotations

import json
import os
from urllib import error, parse, request


def _base_url() -> str:
    return os.getenv("ALMOX_API_BASE_URL", "").strip().rstrip("/")


def is_enabled() -> bool:
    return bool(_base_url()) and os.getenv("ALMOX_API_DISABLE_CLIENT", "0") != "1"


def call_json(
    method: str,
    path: str,
    params: dict[str, object] | None = None,
    payload: dict[str, object] | None = None,
    timeout: int = 8,
) -> tuple[int, object | None]:
    if not is_enabled():
        return 0, None

    base_url = _base_url()
    url = f"{base_url}{path}"
    if params:
        query = parse.urlencode(
            {k: v for k, v in params.items() if v is not None and v != ""}
        )
        if query:
            url = f"{url}?{query}"

    data = None
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("ALMOX_API_KEY", "").strip()
    if api_key:
        headers["x-api-key"] = api_key
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = request.Request(url=url, method=method.upper(), data=data, headers=headers)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8") if resp.length != 0 else ""
            if not body:
                return resp.getcode(), None
            return resp.getcode(), json.loads(body)
    except error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8")
            return exc.code, json.loads(body) if body else None
        except Exception:
            return exc.code, None
    except Exception:
        return 0, None

