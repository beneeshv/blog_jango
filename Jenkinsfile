pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat 'python -m venv .venv'
                bat '.venv\\Scripts\\python -m pip install --upgrade pip setuptools wheel'
                // Install available Pillow version with binary distribution
                bat '.venv\\Scripts\\pip install --only-binary=:all: pillow>=10.0.0'
                // Then install the rest of requirements
                bat '.venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Django Tests') {
            steps {
                bat '.venv\\Scripts\\python manage.py test --noinput'
            }
            post {
                always {
                    junit '**/test-reports/*.xml'
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                bat '.venv\\Scripts\\python manage.py collectstatic --noinput'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed - cleanup can go here'
            // Optional: Clean up the virtual environment
            // bat 'rmdir /s /q .venv'
        }
        success {
            echo '✅ Pipeline succeeded'
        }
        failure {
            echo '❌ Pipeline failed'
        }
    }
}