from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import shutil
import stat
import threading
import time
import uuid

app = FastAPI()

# 🔥 GLOBAL LOG STORAGE
logs = []

# Enable CORS
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


# 🔥 LOG ENDPOINT
@app.get("/logs")
def get_logs():
    return {"logs": logs}


# Windows-safe delete
def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


# 🔥 DEPLOY FUNCTION (FULL FIXED VERSION)
def deploy_repo(repo_url):
    logs.clear()

    def log(msg):
        print(msg)
        logs.append(msg)

    try:
        log("🚀 Starting deployment...")

        os.makedirs("deployments", exist_ok=True)

        # 🔥 UNIQUE FOLDER (avoids Windows lock issues)
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        unique_id = uuid.uuid4().hex[:6]
        repo_path = os.path.join("deployments", f"{repo_name}_{unique_id}")

        # 🔥 CLONE
        log(f"📦 Cloning repo: {repo_url}")

        clone = subprocess.run(
            ["git", "clone", repo_url, repo_path],
            text=True
        )

        if clone.returncode != 0:
            log("❌ Clone failed")
            return

        log("✅ Repo cloned successfully")

        # Ensure Dockerfile exists
        dockerfile_path = os.path.join(repo_path, "Dockerfile")

        if not os.path.exists(dockerfile_path):
            log("🛠 Creating Dockerfile...")
            with open(dockerfile_path, "w") as f:
                f.write("""FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt || true
CMD ["python", "-m", "http.server", "8000"]
""")

        image_name = repo_name.lower()
        container_name = image_name + "-" + unique_id

        # 🔥 BUILD DOCKER
        log("🐳 Building Docker image...")

        build = subprocess.run(
            ["docker", "build", "-t", image_name, repo_path],
            text=True
        )

        if build.returncode != 0:
            log("❌ Docker build failed")
            return

        log("✅ Docker image built")

        # Remove old container (ignore errors)
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            text=True
        )

        # 🔥 RUN CONTAINER
        log("🚀 Running container...")

        run = subprocess.run(
            [
                "docker", "run", "-d",
                "-p", "8001:8000",
                "--name", container_name,
                image_name
            ],
            text=True
        )

        if run.returncode != 0:
            log("❌ Container run failed")
            return

        log("🎉 Deployment successful!")
        log("🌐 App running at: http://localhost:8001")

    except Exception as e:
        log(f"💥 ERROR: {str(e)}")


# 🔥 API ENDPOINT
@app.post("/deploy")
def deploy(data: Repo):
    threading.Thread(target=deploy_repo, args=(data.repo_url,)).start()

    return {
        "status": "Deployment started 🚀",
        "message": "Check logs below",
        "url": "http://localhost:8001"
    }