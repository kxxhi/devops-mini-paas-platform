from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import shutil
import stat

app = FastAPI()

# 🔥 Enable CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Repo(BaseModel):
    repo_url: str


@app.get("/")
def home():
    return {"message": "Mini PaaS Backend Running 🚀"}


# Windows-safe delete
def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


@app.post("/deploy")
def deploy(data: Repo):
    repo_url = data.repo_url

    os.makedirs("deployments", exist_ok=True)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join("deployments", repo_name)

    # Delete old repo
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onerror=remove_readonly)

    # Clone repo
    clone = subprocess.run(
        ["git", "clone", repo_url, repo_path],
        capture_output=True,
        text=True
    )

    if clone.returncode != 0:
        return {"error": clone.stderr}

    # Create Dockerfile if missing
    dockerfile_path = os.path.join(repo_path, "Dockerfile")

    if not os.path.exists(dockerfile_path):
        with open(dockerfile_path, "w") as f:
            f.write("""FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt || true
CMD ["python", "app.py"]
""")

    # Build image
    image_name = repo_name.lower()

    build = subprocess.run(
        ["docker", "build", "-t", image_name, repo_path],
        capture_output=True,
        text=True
    )

    if build.returncode != 0:
        return {
            "error": "Docker build failed",
            "stderr": build.stderr
        }

    # Run container
    run = subprocess.run(
        ["docker", "run", "-d", "-p", "8001:80", image_name],
        capture_output=True,
        text=True
    )

    if run.returncode != 0:
        return {
            "error": "Container run failed",
            "stderr": run.stderr
        }

    return {
        "status": "App deployed successfully 🚀",
        "url": "http://localhost:8001"
    }