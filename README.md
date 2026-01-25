# cicd-budgeting
Use case: Create a end to end cicd pipeline using minio server, jenkins and docker where we are mimicking to load data from source: s3 bucket and do some transformation on the data and loading the processed data back to a different s3 bucket. This job is automated and run using jenkins pipeline using github webhook

1️⃣ Run ``` docker-compose -f docker-compose.yaml up -d```

2️⃣ Install Required Jenkins Plugins

Go to Jenkins → Manage Jenkins → Plugins

Install:

✅ Git

✅ GitHub

✅ GitHub Integration

✅ Pipeline

✅ Docker Pipeline

Restart Jenkins once.

3️⃣ Connect GitHub to Jenkins (Webhook + Credentials)
🔐 Add GitHub credentials

Manage Jenkins → Credentials

Add:

Kind: Username with password

Username: your GitHub username

Password: GitHub Personal Access Token

Scope: Global

(For PAT scopes: repo, admin:repo_hook)

🔔 Create GitHub Webhook

In your GitHub repo:

Settings → Webhooks → Add Webhook


Payload URL:

http://<your-machine-ip>:8080/github-webhook/


(⚠️ localhost won’t work unless tunneled)

Content type: application/json

Events: Just push events

4️⃣ Create Jenkins Pipeline Job

New Item → Pipeline

Pipeline definition:

Pipeline script from SCM

SCM: Git

Repo URL: your GitHub repo

Credentials: GitHub creds

Branch: main

Script path: Jenkinsfile

5️⃣ Jenkinsfile (Docker Pipeline)
Example: build & run Docker image from repo
```
pipeline {
    agent any

    environment {
        IMAGE_NAME = "myapp"
        CONTAINER_NAME = "myapp_container"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    docker build -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh """
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline executed successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
```