#!/usr/bin/env bash
# Roda uma vez, quando o container é criado ou reconstruído.
set -euo pipefail

cd "$(dirname "$0")/.."

# Pastas locais do projeto (credenciais da AWS e cache do pip). Ficam no .gitignore.
mkdir -p .local/aws .local/pip-cache
chmod 700 .local/aws

# Ambiente virtual dentro do projeto. Se já existir, é reaproveitado.
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt

echo
echo "Ambiente pronto:"
.venv/bin/python --version
.venv/bin/python -m pip --version
aws --version
