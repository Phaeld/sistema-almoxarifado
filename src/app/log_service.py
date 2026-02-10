"""
====================================================================
    LOG SERVICE (AES)
--------------------------------------------------------------------
    Registra eventos do sistema em arquivo criptografado (AES-GCM).
====================================================================
"""

import os
import base64
from datetime import datetime
from pathlib import Path

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes


PASSWORD = "SysLog26@obras_"
PBKDF2_ROUNDS = 200_000


class LogService:
    @staticmethod
    def _project_root() -> Path:
        return Path(os.getcwd()).resolve()

    @staticmethod
    def _log_path() -> Path:
        return LogService._project_root() / "logs" / "syslog.enc"

    @staticmethod
    def _format_line(user, action, details):
        username = (user or {}).get("username") if isinstance(user, dict) else None
        name = (user or {}).get("name") if isinstance(user, dict) else None
        tag = (user or {}).get("tag") if isinstance(user, dict) else None
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return f"[{timestamp}] user={username} name={name} tag={tag} action={action} details={details}"

    @staticmethod
    def _get_or_create_salt(path: Path) -> bytes:
        if path.exists():
            with path.open("rb") as f:
                header = f.readline().strip()
                if header.startswith(b"SALT:"):
                    return base64.b64decode(header[5:])
        salt = get_random_bytes(16)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            f.write(b"SALT:" + base64.b64encode(salt) + b"\n")
        return salt

    @staticmethod
    def _derive_key(salt: bytes) -> bytes:
        return PBKDF2(PASSWORD, salt, dkLen=32, count=PBKDF2_ROUNDS)

    @staticmethod
    def log_event(action, details="", user=None):
        path = LogService._log_path()
        salt = LogService._get_or_create_salt(path)
        key = LogService._derive_key(salt)

        line = LogService._format_line(user, action, details)
        nonce = get_random_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(line.encode("utf-8"))
        payload = nonce + tag + ciphertext
        encoded = base64.b64encode(payload)

        with path.open("ab") as f:
            f.write(encoded + b"\n")
