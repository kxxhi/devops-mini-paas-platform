from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import stat
import threading
import uuid
import socket

app = FastAPI()

logs = []

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


@app.get("/logs")
def get_logs():
    return {"logs": logs}


def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def deploy_repo(repo_url):
    logs.clear()

    def log(msg):
        print(msg)
        logs.append(msg)

    try:
        log("🚀 Starting deployment...")

        os.makedirs("deployments", exist_ok=True)

        repo_name = repo_url.split("/")[-1].replace(".git", "")
        unique_id = uuid.uuid4().hex[:6]
        repo_path = os.path.join("deployments", f"{repo_name}_{unique_id}")

        # 🔹 Clone repo
        log(f"📦 Cloning repo: {repo_url}")
        clone = subprocess.run(
            ["git", "clone", repo_url, repo_path],
            capture_output=True,
            text=True
        )

        if clone.returncode != 0:
            log("❌ Clone failed")
            log(clone.stderr)
            return

        log("✅ Repo cloned successfully")

        # 🔥 Dockerfile override (FINAL FIX)
        dockerfile_path = os.path.join(repo_path, "Dockerfile")
        log("🛠 Overriding Dockerfile...")

        with open(dockerfile_path, "w") as f:
            f.write("""FROM python:3.11
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install django gunicorn whitenoise dj-database-url psycopg2-binary || true
RUN pip install -r requirements.txt || true

CMD ["sh", "-c", "if [ -f package.json ]; then npm install && npm start; elif [ -f manage.py ]; then python manage.py migrate --run-syncdb 2>/dev/null || true && gunicorn --bind 0.0.0.0:8000 gettingstarted.wsgi; elif [ -f app.py ]; then python app.py; elif [ -f main.py ]; then python main.py; else python -m http.server 8000; fi"]
""")

        image_name = repo_name.lower()
        container_name = f"{image_name}-{unique_id}"

        # 🔹 Build image
        log("🐳 Building Docker image...")
        build = subprocess.run(
            ["docker", "build", "-t", image_name, repo_path],
            capture_output=True,
            text=True
        )

        if build.returncode != 0:
            log("❌ Docker build failed")
            log(build.stderr)
            return

        log("✅ Docker image built")

        # Remove old container
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            capture_output=True,
            text=True
        )

        # 🔥 Find free port (FIXED)
        port = 8001
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) != 0:
                    break
                port += 1

        log(f"📡 Using port: {port}")

        # 🔹 Run container
        log("🚀 Running container...")
        run = subprocess.run(
            [
                "docker", "run", "-d",
                "-p", f"{port}:8000",
                "--name", container_name,
                image_name
            ],
            capture_output=True,
            text=True
        )

        if run.returncode != 0:
            log("❌ Container run failed")
            log(run.stderr)
            return

        log("🎉 Deployment successful!")
        log(f"🌐 App running at: http://localhost:{port}")

    except Exception as e:
        log(f"💥 ERROR: {str(e)}")


@app.post("/deploy")
def deploy(data: Repo):
    threading.Thread(target=deploy_repo, args=(data.repo_url,)).start()

    return {
        "status": "Deployment started 🚀",
        "message": "Check logs endpoint",
        "logs_url": "http://127.0.0.1:8000/logs"
    }