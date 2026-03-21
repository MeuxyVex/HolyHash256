"""Exemple d'integration Python via ctypes pour une lib native HolyC.

Usage :
    python3 python_ctypes_example.py [texte] [chemin/vers/libholyc_hash.so]

Tu peux aussi definir la variable d'environnement HOLYC_HASH_LIB.
"""

from __future__ import annotations

import ctypes
import os
import sys
from pathlib import Path

DEFAULT_TEXT = "bonjour tout le monde"
DEFAULT_LIB_NAMES = ("libholyc_hash.so", "a.so")


def candidate_library_paths(explicit_path: str | None = None) -> list[Path]:
    candidates: list[Path] = []

    if explicit_path:
        candidates.append(Path(explicit_path).expanduser())

    env_path = os.environ.get("HOLYC_HASH_LIB")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    cwd = Path.cwd()
    for name in DEFAULT_LIB_NAMES:
        candidates.append(cwd / name)

    return candidates


def looks_like_shared_library(path: Path) -> bool:
    return path.suffix == ".so" or ".so." in path.name


def load_library(explicit_path: str | None = None) -> ctypes.CDLL:
    tried: list[Path] = []
    load_errors: list[str] = []

    for candidate in candidate_library_paths(explicit_path):
        resolved = candidate.resolve()
        tried.append(resolved)

        if not resolved.exists():
            continue

        if not looks_like_shared_library(resolved):
            load_errors.append(f"{resolved} (ignore: fichier existant mais pas une bibliotheque .so)")
            continue

        try:
            return ctypes.CDLL(str(resolved))
        except OSError as exc:
            load_errors.append(f"{resolved} ({exc})")

    tried_str = "\n - ".join(str(path) for path in tried)
    details = ""
    if load_errors:
        details = "\nErreurs de chargement :\n - " + "\n - ".join(load_errors)

    raise FileNotFoundError(
        "Aucune bibliotheque native chargeable trouvee.\n"
        "Compile ou genere d'abord une librairie partagee HolyC (.so), puis passe son chemin en argument\n"
        "ou via HOLYC_HASH_LIB.\n"
        f"Chemins tries :\n - {tried_str}"
        f"{details}"
    )


def build_hasher(lib: ctypes.CDLL):
    lib.HashTextHex.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
    lib.HashTextHex.restype = None

    def hash_text(text: str) -> str:
        raw = text.encode("utf-8")
        out = ctypes.create_string_buffer(65)
        lib.HashTextHex(raw, out)
        return out.value.decode("ascii")

    return hash_text


def main(argv: list[str]) -> int:
    text = DEFAULT_TEXT
    lib_path = None

    if len(argv) >= 2:
        text = argv[1]
    if len(argv) >= 3:
        lib_path = argv[2]

    try:
        library = load_library(lib_path)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    hash_text = build_hasher(library)
    print(hash_text(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
