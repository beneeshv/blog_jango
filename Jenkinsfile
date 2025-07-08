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
                // Install Pillow first with binary to avoid compilation issues
                bat '.venv\\Scripts\\pip install --only-binary=:all: pillow==10.3.0'
                // Then install the rest of requirements
                bat '.venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Django Tests') {
            steps {
                script {
                    try {
                        bat '.venv\\Scripts\\python manage.py test --noinput'
                    } catch (Exception e) {
                        echo "❌ Tests failed: ${e}"
                        currentBuild.result = 'FAILURE'
                        error('Tests failed')
                    }
                }
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