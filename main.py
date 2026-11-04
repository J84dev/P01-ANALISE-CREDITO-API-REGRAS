import hmac
import json
import os
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from mangum import Mangum

API_KEY = os.environ["API_KEY"]
REGRAS_VERSAO = os.environ["REGRAS_VERSAO"]

arquivo = Path(__file__).parent / "regras" / f"regras-{REGRAS_VERSAO}.json"
REGRAS = json.loads(arquivo.read_text(encoding="utf-8"))

cabecalho_da_chave = APIKeyHeader(name="x-api-key", auto_error=False)


def exigir_chave(chave: str | None = Depends(cabecalho_da_chave)) -> None:
    if not chave or not hmac.compare_digest(chave.encode(), API_KEY.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API ausente ou inválida.",
        )


expor_docs = os.environ.get("API_DOCS") == "1"
app = FastAPI(
    title="API de regras de crédito",
    docs_url="/docs" if expor_docs else None,
    redoc_url=None,
    openapi_url="/openapi.json" if expor_docs else None,
)


@app.get("/regras", dependencies=[Depends(exigir_chave)])
def obter_regras():
    return JSONResponse(REGRAS, headers={"Cache-Control": "no-store"})


handler = Mangum(app, lifespan="off")
