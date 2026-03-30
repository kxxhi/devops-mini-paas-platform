from fastapi import FastAPI
from pydantic import BaseModel
import os
import subprocess
import shutil
import stat

app = FastAPI()

# Request model
class Repo(BaseModel):
    repo_url: str


@app.get("/")
def home():
    return {"message": "Mini PaaS Backend Running 🚀"}


# 🔹 Windows-safe delete function
def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


@app.post("/deploy")
def deploy(data: Repo):
    repo_url = data.repo_url

    # Create deployments folder
    os.makedirs("deployments", exist_ok=True)

    # Extract repo name
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join("deployments", repo_name)

    # 🔥 Remove old repo (safe delete)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onerror=remove_readonly)

    # 🔹 STEP 1: Clone repo
    clone = subprocess.run(
        ["git", "clone", repo_url, repo_path],
        capture_output=True,
        text=True
    )

    if clone.returncode != 0:
        return {
            "error": "Git clone failed",
            "details": clone.stderr
        }

    # 🔹 STEP 2: Ensure Dockerfile exists
    dockerfile_path = os.path.join(repo_path, "Dockerfile")

    # 🔥 Auto-create Dockerfile if missing
    if not os.path.exists(dockerfile_path):
        with open(dockerfile_path, "w") as f:
            f.write("""FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt || true
CMD ["python", "app.py"]
""")

    # 🔹 STEP 3: Build Docker image
    image_name = repo_name.lower()

    build = subprocess.run(
        ["docker", "build", "-t", image_name, repo_path],
        capture_output=True,
        text=True
    )

    if build.returncode != 0:
        return {
            "error": "Docker build failed",
            "stdout": build.stdout,
            "stderr": build.stderr
        }

    return {
        "status": "Docker image built successfully 🚀",
        "image": image_name
    }