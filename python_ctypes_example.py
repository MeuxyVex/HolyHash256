"""Exemple d'integration Python pour le hash HolyC.

Le script prefere une bibliotheque partagee (`.so`) via `ctypes`,
mais peut aussi retomber sur un executable CLI (par ex. `a.out`) via `subprocess`.

Usage :
    python3 python_ctypes_example.py [texte] [chemin/vers/libholyc_hash.so|./a.out]

Tu peux aussi definir :
- HOLYC_HASH_LIB pour un `.so`
- HOLYC_HASH_EXE pour un executable CLI
"""

from __future__ import annotations

import ctypes
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_TEXT = "bonjour tout le monde"
DEFAULT_LIB_NAMES = ("libholyc_hash.so", "a.so")
DEFAULT_EXE_NAMES = ("a.out", "hashage", "hashage.out")
HASH_PREFIX = "Hash (hex) : "


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


def candidate_executable_paths(explicit_path: str | None = None) -> list[Path]:
    candidates: list[Path] = []

    if explicit_path:
        candidates.append(Path(explicit_path).expanduser())

    env_path = os.environ.get("HOLYC_HASH_EXE")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    cwd = Path.cwd()
    for name in DEFAULT_EXE_NAMES:
        candidates.append(cwd / name)

    return candidates


def looks_like_shared_library(path: Path) -> bool:
    return path.suffix == ".so" or ".so." in path.name


def looks_like_executable(path: Path) -> bool:
    return path.exists() and path.is_file() and os.access(path, os.X_OK)


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


def load_executable(explicit_path: str | None = None) -> Path:
    tried: list[Path] = []

    for candidate in candidate_executable_paths(explicit_path):
        resolved = candidate.resolve()
        tried.append(resolved)
        if looks_like_executable(resolved):
            return resolved

    tried_str = "\n - ".join(str(path) for path in tried)
    raise FileNotFoundError(
        "Aucun executable HolyC utilisable trouve pour le mode CLI.\n"
        "Passe le chemin de l'executable en argument ou via HOLYC_HASH_EXE.\n"
        f"Chemins tries :\n - {tried_str}"
    )


def build_ctypes_hasher(lib: ctypes.CDLL):
    lib.HashTextHex.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
    lib.HashTextHex.restype = None

    def hash_text(text: str) -> str:
        raw = text.encode("utf-8")
        out = ctypes.create_string_buffer(65)
        lib.HashTextHex(raw, out)
        return out.value.decode("ascii")

    return hash_text


def build_cli_hasher(executable: Path):
    def hash_text(text: str) -> str:
        completed = subprocess.run(
            [str(executable)],
            input=text + "\n",
            text=True,
            capture_output=True,
            check=False,
        )

        for line in completed.stdout.splitlines():
            marker = line.find(HASH_PREFIX)
            if marker != -1:
                return line[marker + len(HASH_PREFIX) :].strip()

        raise RuntimeError(
            "Execution CLI echouee ou sortie inattendue : impossible de trouver la ligne de hash.\n"
            f"Code retour : {completed.returncode}\n"
            f"Stdout :\n{completed.stdout}\n"
            f"Stderr :\n{completed.stderr}"
        )

    return hash_text


def build_hasher(explicit_path: str | None = None):
    try:
        return build_ctypes_hasher(load_library(explicit_path)), "ctypes"
    except FileNotFoundError as lib_exc:
        try:
            return build_cli_hasher(load_executable(explicit_path)), "cli"
        except FileNotFoundError as exe_exc:
            raise FileNotFoundError(f"{lib_exc}\n\nFallback CLI impossible :\n{exe_exc}") from exe_exc


def main(argv: list[str]) -> int:
    text = DEFAULT_TEXT
    path_hint = None

    if len(argv) >= 2:
        text = argv[1]
    if len(argv) >= 3:
        path_hint = argv[2]

    try:
        hash_text, backend = build_hasher(path_hint)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"Backend utilise : {backend}", file=sys.stderr)
    try:
        result = hash_text(text)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
