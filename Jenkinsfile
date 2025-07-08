pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        PIP = ".venv\\Scripts\\pip.exe"
        PYTHON = ".venv\\Scripts\\python.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat "python -m venv %VENV_DIR%"
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "%PIP% install --upgrade pip"
                bat "%PIP% install -r requirements.txt"
            }
        }

        stage('Run Migrations') {
            steps {
                bat "%PYTHON% manage.py makemigrations"
                bat "%PYTHON% manage.py migrate"
            }
        }

        stage('Run Tests') {
            steps {
                bat "%PYTHON% manage.py test"
            }
        }

        stage('Collect Static Files') {
            steps {
                bat "%PYTHON% manage.py collectstatic --noinput"
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t django-app ."
            }
        }
    }

    post {
        failure {
            echo "❌ Build failed."
        }
        success {
            echo "✅ Build succeeded!"
        }
    }
}
