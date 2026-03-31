from fastapi import FastAPI
from pydantic import BaseModel
import os
import subprocess
import shutil
import stat
import threading

app = FastAPI()


# Request model
class Repo(BaseModel):
    repo_url: str


@app.get("/")
def home():
    return {"message": "Mini PaaS Backend Running 🚀"}


# Windows-safe delete
def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


# 🔥 BACKGROUND DEPLOY FUNCTION
def deploy_repo(repo_url):
    os.makedirs("deployments", exist_ok=True)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join("deployments", repo_name)

    # Remove old repo
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, onerror=remove_readonly)

    # Clone repo
    subprocess.run(["git", "clone", repo_url, repo_path])

    # Ensure Dockerfile exists
    dockerfile_path = os.path.join(repo_path, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        with open(dockerfile_path, "w") as f:
            f.write("""FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt || true
CMD ["python", "-m", "http.server", "8000"]
""")

    image_name = repo_name.lower()

    # Build Docker image
    subprocess.run(["docker", "build", "-t", image_name, repo_path])

    container_name = image_name + "-container"

    # 🔥 FIX: Remove old container automatically
    subprocess.run(
        ["docker", "rm", "-f", container_name],
        capture_output=True,
        text=True
    )

    # Run container
    subprocess.run([
        "docker", "run", "-d",
        "-p", "8001:8000",
        "--name", container_name,
        image_name
    ])


# 🔥 FAST NON-BLOCKING ENDPOINT
@app.post("/deploy")
def deploy(data: Repo):
    threading.Thread(target=deploy_repo, args=(data.repo_url,)).start()

    return {
        "status": "Deployment started 🚀",
        "message": "App will be live in ~1 minute at http://localhost:8001"
    }