import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

raiz = Path(__file__).parent
build = raiz / "build"
destino = raiz / "lambda.zip"

shutil.rmtree(build, ignore_errors=True)
destino.unlink(missing_ok=True)
build.mkdir()

subprocess.run(
    [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        str(raiz / "requirements.txt"),
        "-t",
        str(build),
        "--platform",
        "manylinux2014_x86_64",
        "--only-binary=:all:",
        "--python-version",
        "3.13",
        "--implementation",
        "cp",
    ],
    check=True,
)

shutil.copy(raiz / "main.py", build / "main.py")
shutil.copytree(raiz / "regras", build / "regras")

with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
    for arquivo in build.rglob("*"):
        if arquivo.is_file() and "__pycache__" not in arquivo.parts:
            z.write(arquivo, arquivo.relative_to(build).as_posix())

print(f"Pronto: {destino} ({destino.stat().st_size / 1_000_000:.1f} MB)")
