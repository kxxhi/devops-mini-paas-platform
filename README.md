# 🚀 Mini PaaS Platform with CI/CD using Jenkins & Docker

## 📌 Project Overview
This project implements a **Mini Platform as a Service (PaaS)** that automates application deployment using a CI/CD pipeline. It integrates **Jenkins, Docker, FastAPI, and Pytest** to enable automated testing, containerization, and deployment of applications from a GitHub repository.

---

## 🎯 Features

- 🔹 Automated CI/CD pipeline using Jenkins  
- 🔹 GitHub integration for source code management  
- 🔹 Automated dependency installation  
- 🔹 Backend API testing using Pytest  
- 🔹 Docker-based containerization and deployment  
- 🔹 Real-time deployment logs  
- 🔹 Error handling for invalid repositories  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)  
- **Testing:** Pytest  
- **CI/CD Tool:** Jenkins  
- **Containerization:** Docker  
- **Version Control:** Git & GitHub  

---

## 🧠 System Architecture
# 🚀 Mini PaaS Platform with CI/CD using Jenkins & Docker

## 📌 Project Overview
This project implements a **Mini Platform as a Service (PaaS)** that automates application deployment using a CI/CD pipeline. It integrates **Jenkins, Docker, FastAPI, and Pytest** to enable automated testing, containerization, and deployment of applications from a GitHub repository.

---

## 🎯 Features

- 🔹 Automated CI/CD pipeline using Jenkins  
- 🔹 GitHub integration for source code management  
- 🔹 Automated dependency installation  
- 🔹 Backend API testing using Pytest  
- 🔹 Docker-based containerization and deployment  
- 🔹 Real-time deployment logs  
- 🔹 Error handling for invalid repositories  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)  
- **Testing:** Pytest  
- **CI/CD Tool:** Jenkins  
- **Containerization:** Docker  
- **Version Control:** Git & GitHub  

---

## 🧠 System Architecture
# 🚀 Mini PaaS Platform with CI/CD using Jenkins & Docker

## 📌 Project Overview
This project implements a **Mini Platform as a Service (PaaS)** that automates application deployment using a CI/CD pipeline. It integrates **Jenkins, Docker, FastAPI, and Pytest** to enable automated testing, containerization, and deployment of applications from a GitHub repository.

---

## 🎯 Features

- 🔹 Automated CI/CD pipeline using Jenkins  
- 🔹 GitHub integration for source code management  
- 🔹 Automated dependency installation  
- 🔹 Backend API testing using Pytest  
- 🔹 Docker-based containerization and deployment  
- 🔹 Real-time deployment logs  
- 🔹 Error handling for invalid repositories  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)  
- **Testing:** Pytest  
- **CI/CD Tool:** Jenkins  
- **Containerization:** Docker  
- **Version Control:** Git & GitHub  

---

## 🧠 System Architecture
User → GitHub Repo → Jenkins Pipeline → Test → Docker Build → Deploy Container → Running App


---

## ⚙️ Workflow

1. Jenkins pipeline is triggered manually  
2. Repository is cloned from GitHub  
3. Dependencies are installed using `requirements.txt`  
4. Test cases are executed using Pytest  
5. Docker image is built  
6. Container is deployed and application runs locally  

---

## 📂 Project Structure

---

## ⚙️ Workflow

1. Jenkins pipeline is triggered manually  
2. Repository is cloned from GitHub  
3. Dependencies are installed using `requirements.txt`  
4. Test cases are executed using Pytest  
5. Docker image is built  
6. Container is deployed and application runs locally  

---

## 📂 Project Structure

devops-mini-paas-platform/
│
├── backend/
│ ├── main.py
│ ├── test_main.py
│ ├── requirements.txt
│ ├── Dockerfile
│
├── frontend/
│ ├── index.html
│
└── README.md

---

## 🧪 Testing

- Automated test cases are written using **Pytest**
- Includes:
  - ✅ API endpoint testing  
  - ✅ Deployment success testing  
  - ❌ Invalid repository handling  

Example:

```bash
pytest backend/test_main.py
