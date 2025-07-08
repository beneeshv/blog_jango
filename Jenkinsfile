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

        stage('Set Up Python') {
            steps {
                bat "python -m venv ${VENV}"
                bat "${VENV}\\Scripts\\pip install --upgrade pip"
                bat "${VENV}\\Scripts\\pip install -r requirements.txt"
            }
        }

        stage('Run Tests') {
            steps {
                bat "${VENV}\\Scripts\\python manage.py test"
            }
        }

        stage('Run Server for 20 sec') {
            steps {
                bat """
                start /b ${VENV}\\Scripts\\python manage.py runserver 0.0.0.0:8000
                timeout /t 20
                taskkill /f /im python.exe
                """
            }
        }
    }

    post {
        success {
            echo "✅ Server ran successfully for 20 seconds!"
        }
        failure {
            echo "❌ Server stage failed."
        }
    }
}
