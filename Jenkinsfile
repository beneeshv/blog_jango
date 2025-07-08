pipeline {
    agent any
    environment {
        VENV = ".venv"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                bat "python -m venv %VENV%"
                bat "%VENV%\\Scripts\\pip install --upgrade pip"
                bat "%VENV%\\Scripts\\pip install -r requirements.txt"
            }
        }
        stage('Run Django Tests') {
            steps {
                bat "%VENV%\\Scripts\\python manage.py test"
            }
        }
    }
    post {
        success {
            echo '✅ Tests ran successfully!'
        }
        failure {
            echo '❌ Tests failed.'
        }
    }
}
