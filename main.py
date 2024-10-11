import jwt
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY_JWT = "j&4*F7j3l!2Nf4#skl09@3nl1nj&BHJKNJKDNAn&8#3G@Hsj"

# Modelo de dados para o registro do usuário
class Usuario(BaseModel):
    nome: str
    email: str
    senha: str

# Função para criar o JWT
def criar_jwt(usuario: Usuario):
    payload = {
        "sub": usuario.email,  # O subject (sub) do token é o email do usuário
        "name": usuario.nome,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expiração de 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY_JWT, algorithm="HS256")
    return token

# Rota de exemplo
@app.post("/registrar")
async def registrar(usuario: Usuario):
    token = criar_jwt(usuario)
    
    return {
        "jwt": token
    }
