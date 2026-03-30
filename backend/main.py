from fastapi import FastAPI
import subprocess   # <-- ADD THIS

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mini PaaS Backend Running 🚀"}

@app.post("/deploy")
def deploy(repo_url: str):
    result = subprocess.run(
        ["git", "clone", repo_url],
        capture_output=True,
        text=True
    )

    return {
        "status": "Repo cloned",
        "output": result.stdout,
        "error": result.stderr
    }