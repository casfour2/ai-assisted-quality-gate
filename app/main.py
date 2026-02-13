from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


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

@app.get("/ui", response_class=HTMLResponse)
def simple_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI QA Demo App</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .card { padding: 20px; border: 1px solid #ccc; border-radius: 8px; width: 300px; }
            .success { color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>AI QA Demo Dashboard</h1>

        <div class="card">
            <h3>Health Check</h3>
            <button onclick="checkHealth()">Check Health</button>
            <p id="healthResult"></p>
        </div>

        <br/>

        <div class="card">
            <h3>Login</h3>
            <input id="username" placeholder="Username"/><br/><br/>
            <input id="password" type="password" placeholder="Password"/><br/><br/>
            <button onclick="login()">Login</button>
            <p id="loginResult"></p>
        </div>

        <script>
            async function checkHealth() {
                const response = await fetch("/health");
                const data = await response.json();
                document.getElementById("healthResult").innerHTML =
                    "<span class='success'>Status: " + data.status + "</span>";
            }

            async function login() {
                const username = document.getElementById("username").value;
                const password = document.getElementById("password").value;

                const response = await fetch("/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });

                const resultEl = document.getElementById("loginResult");

                if (response.status === 200) {
                    const data = await response.json();
                    resultEl.innerHTML =
                        "<span class='success'>Token: " + data.token + "</span>";
                } else {
                    resultEl.innerHTML =
                        "<span class='error'>Invalid credentials</span>";
                }
            }
        </script>
    </body>
    </html>
    """