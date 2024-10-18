from jose import jwt  # Usando a biblioteca python-jose para JWT
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import bcrypt

# Configuração da aplicação FastAPI
app = FastAPI()

# Definir a chave secreta para assinar os tokens JWT
SECRET_KEY_JWT = "j&4*F7j3l!2Nf4#skl09@3nl1nj&BHJKNJKDNAn&8#3G@Hsj"

# Configuração do banco de dados PostgreSQL
DATABASE_URL = "postgresql://cloud:cloud@db:5432/db"

# Criando a engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Criando a base para modelos ORM
Base = declarative_base()

# Criando uma sessão para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo de usuário para o banco de dados
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Modelo de dados recebido pela API
class Usuario(BaseModel):
    nome: str
    email: str
    senha: str

# Modelo de dados para o login
class LoginData(BaseModel):
    email: str
    senha: str

# Função para criar o JWT usando python-jose
def criar_jwt(usuario: Usuario):
    payload = {
        "sub": usuario.email,  # O subject (sub) do token é o email do usuário
        "name": usuario.nome,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expiração de 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY_JWT, algorithm="HS256")  # Usando a biblioteca jose
    return token


# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para salvar o usuário no banco de dados
def criar_usuario(db: Session, usuario: Usuario):
    try:
        # Gerando um hash seguro da senha
        senha_hash = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
        db_usuario = UsuarioDB(nome=usuario.nome, email=usuario.email, senha_hash=senha_hash.decode('utf-8'))
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

# Função para listar todos os usuários
@app.get("/")
async def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioDB).all()  # Consulta todos os usuários no banco de dados
    return [{"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "senha_hash": usuario.senha_hash} for usuario in usuarios]

# Rota para registrar o usuário
@app.post("/registrar")
async def registrar(usuario: Usuario, db: Session = Depends(get_db)):
    # Verifica se o email já existe no banco de dados
    db_usuario = db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=409, detail="Email já registrado")
    
    # Salva o usuário no banco
    criar_usuario(db, usuario)
    
    # Gerar o token JWT
    token = criar_jwt(usuario)
    
    return {
        "jwt": token
    }

# Endpoint para login
@app.post("/login")
async def login(login_data: LoginData, db: Session = Depends(get_db)):
    # Verifica se o usuário existe no banco de dados
    db_usuario = db.query(UsuarioDB).filter(UsuarioDB.email == login_data.email).first()
    if not db_usuario:
        raise HTTPException(status_code=401, detail="Email não encontrado")
    
    # Verifica se a senha está correta
    if not bcrypt.checkpw(login_data.senha.encode('utf-8'), db_usuario.senha_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail=" Email e senha não confere")
    
    # Gerar o token JWT
    token = criar_jwt(db_usuario)
    
    return {
        "jwt": token
    }
