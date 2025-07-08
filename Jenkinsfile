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

        stage('Run Hello World Test') {
            steps {
                bat "${VENV}\\Scripts\\python manage.py test blog.tests.HelloWorldTest"
            }
        }
    }

    post {
        success {
            echo "✅ Hello World test ran successfully!"
        }
        failure {
            echo "❌ Hello World test failed."
        }
    }
}
