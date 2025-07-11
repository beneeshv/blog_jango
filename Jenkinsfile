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
          stage('Build Docker Image') {
    steps {
        bat 'docker build -t beneesh/blog .'
    }
}

stage('Push to Docker Hub') {
    steps {
        withCredentials([usernamePassword(
            credentialsId: '76492620-2fd6-45e1-901c-383958bf196d', 
            usernameVariable: 'beneesh', 
            passwordVariable: '@Be23ne10esh'
        )]) {
            bat '''
                docker login -u %beneesh% -p %@Be23ne10esh%
                docker push beneesh/blog
            '''
        }
    }
}
    }

    
}