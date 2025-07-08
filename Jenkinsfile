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
                // Install Pillow first with binary distribution
                bat '.venv\\Scripts\\pip install --only-binary=:all: pillow>=10.0.0'
                // Then install the rest of requirements
                bat '.venv\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Run Django Tests') {
            steps {
                script {
                    try {
                        // Create test directory if it doesn't exist
                        bat 'mkdir test-reports || echo "Directory exists"'
                        // Run tests with XML output
                        bat '.venv\\Scripts\\python manage.py test --noinput --verbosity=2 --testrunner="xmlrunner.extra.djangotestrunner.XMLTestRunner" --output-file=test-reports/junit.xml'
                    } catch (Exception e) {
                        echo "Test execution failed: ${e}"
                        // Continue pipeline even if tests fail
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
            post {
                always {
                    junit 'test-reports/*.xml'
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
            // Clean up the virtual environment if needed
            // bat 'rmdir /s /q .venv'
        }
        success {
            echo '✅ Pipeline succeeded'
        }
        failure {
            echo '❌ Pipeline failed'
        }
        unstable {
            echo '⚠️ Pipeline completed with unstable status (tests failed)'
        }
    }
}