pipeline {
    agent any

    environment {
        VENV = ".venv"
        PYTHON = "${VENV}/Scripts/python.exe"
        PIP = "${VENV}/Scripts/pip.exe"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat 'python -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "${PIP} install --upgrade pip"
                bat "${PIP} install -r requirements.txt"
            }
        }

        stage('Run Migrations') {
            steps {
                bat "${PYTHON} manage.py migrate"
            }
        }

        stage('Run Tests') {
            steps {
                bat "${PYTHON} manage.py test"
            }
        }

        stage('Collect Static Files') {
            steps {
                bat "${PYTHON} manage.py collectstatic --noinput"
            }
        }

        stage('Build Docker Image') {
            when {
                expression { fileExists('Dockerfile') }
            }
            steps {
                bat 'docker build -t django-app .'
            }
        }
    }

    post {
        success {
            echo '✅ Build completed successfully.'
        }
        failure {
            echo '❌ Build failed.'
        }
    }
}
