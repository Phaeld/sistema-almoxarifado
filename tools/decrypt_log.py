"""
Decrypt syslog.enc and output plaintext lines.
Usage:
  python tools/decrypt_log.py
"""

import base64
from pathlib import Path
from getpass import getpass

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2


PBKDF2_ROUNDS = 200_000


def main():
    project_root = Path(__file__).resolve().parents[1]
    log_path = project_root / "logs" / "syslog.enc"
    out_path = project_root / "logs" / "syslog_decoded.txt"

    if not log_path.exists():
        print(f"Nao encontrado: {log_path}")
        return

    with log_path.open("rb") as f: 
        header = f.readline().strip()
        if not header.startswith(b"SALT:"):
            print("Arquivo invalido: sem SALT.")
            return
        salt = base64.b64decode(header[5:])
        lines = f.read().splitlines()

    password = getpass("Senha do log: ")
    key = PBKDF2(password, salt, dkLen=32, count=PBKDF2_ROUNDS)

    decoded_lines = []
    for line in lines:
        if not line.strip():
            continue
        data = base64.b64decode(line)
        nonce = data[:12]
        tag = data[12:28]
        ciphertext = data[28:]
        try:
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            decoded_lines.append(plaintext.decode("utf-8", errors="replace"))
        except Exception:
            decoded_lines.append("[ERRO] linha nao pode ser descriptografada.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(decoded_lines), encoding="utf-8")
    print(f"OK: {out_path}")


if __name__ == "__main__":
    main()
