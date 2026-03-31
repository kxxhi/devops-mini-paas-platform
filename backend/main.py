from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import shutil
import stat
import threading

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
# Windows-safe delete
def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


@app.post("/deploy")
def deploy(data: Repo):
    repo_url = data.repo_url

# 🔥 BACKGROUND DEPLOY FUNCTION
def deploy_repo(repo_url):
    os.makedirs("deployments", exist_ok=True)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join("deployments", repo_name)

    # Delete old repo
    # Remove old repo
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
    # Clone repo
    subprocess.run(["git", "clone", repo_url, repo_path])

    # Create Dockerfile if missing
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

    # Build image
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

    if build.returncode != 0:
        return {
            "error": "Docker build failed",
            "stderr": build.stderr
        }
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
        "status": "Deployment started 🚀",
        "message": "App will be live in ~1 minute at http://localhost:8001"
    }