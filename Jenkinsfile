pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\NEELGAGAN B R\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
        PYTHONUNBUFFERED = '1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out Playwright-Pytest project...'
            }
        }

        stage('Check Python') {
            steps {
                bat '''
                    "%PYTHON%" --version
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                    if exist .jenkins-venv rmdir /s /q .jenkins-venv
                    "%PYTHON%" -m venv .jenkins-venv
                    .jenkins-venv\\Scripts\\python.exe -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    .jenkins-venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Install Playwright Browsers') {
            steps {
                bat '''
                    .jenkins-venv\\Scripts\\python.exe -m playwright install chromium
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    .jenkins-venv\\Scripts\\python.exe -m pytest -v
                '''
            }
        }
    }

    post {
        always {
            echo 'Jenkins test execution completed.'
        }

        success {
            echo 'All Playwright-Pytest tests passed successfully.'
        }

        failure {
            echo 'Playwright-Pytest execution failed. Check the console output.'
        }
    }
}
