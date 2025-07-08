pipeline {
    agent any

    environment {
        // Use a virtual environment path
        VENV = ".venv"
        PYTHON = "${VENV}/Scripts/python.exe" // for Windows
        PIP = "${VENV}/Scripts/pip.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/your-username/your-django-repo.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv .venv'
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

        stage('Static Files') {
            steps {
                bat "${PYTHON} manage.py collectstatic --noinput"
            }
        }

        // Optional Docker Build
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
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Build succeeded.'
        }
        failure {
            echo 'Build failed.'
        }
    }
}
