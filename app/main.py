from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

app = FastAPI(
    title="AI QA Demo App",
    version="0.1.0"
)
@app.get("/")
def root():
    return {"message": "Welcome to the AI QA Demo App!"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "secret":
        return {"token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")