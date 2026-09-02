pipeline {
    agent any

    environment {
        TEST_ENV = 'dev'
        BROWSER = 'chromium'
        HEADLESS = 'true'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://your-git-repo-url.git'
            }
        }

        stage('Setup Python') {
            steps {
                bat '''
                    python --version
                    python -m venv .venv
                    .\.venv\Scripts\python.exe -m pip install --upgrade pip
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
                    .\.venv\Scripts\python.exe -m playwright install chromium
                '''
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                    mkdir reports
                    .\.venv\Scripts\python.exe -m pytest tests -q --junitxml=reports\junit.xml
                '''
            }
        }
    }

    post {
        always {
            junit 'reports\\junit.xml'
            archiveArtifacts artifacts: 'test-results/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
    }
}
