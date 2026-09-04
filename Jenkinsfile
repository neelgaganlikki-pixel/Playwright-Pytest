pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\NEELGAGAN B R\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
        PYTHONUNBUFFERED = '1'

        TEST_ENV = 'dev'

        DEV_BASE_URL = 'https://opensource-demo.orangehrmlive.com'
        DEV_USERNAME = 'Admin'
        DEV_PASSWORD = 'admin123'

        QA_BASE_URL = 'https://opensource-demo.orangehrmlive.com'
        QA_USERNAME = 'Admin'
        QA_PASSWORD = 'admin123'

        UAT_BASE_URL = 'https://opensource-demo.orangehrmlive.com'
        UAT_USERNAME = 'Admin'
        UAT_PASSWORD = 'admin123'

        PROD_BASE_URL = 'https://opensource-demo.orangehrmlive.com'
        PROD_USERNAME = 'Admin'
        PROD_PASSWORD = 'admin123'

        BROWSER = 'chromium'
        HEADLESS = 'true'
        SLOW_MO = '0'

        SCREENSHOT_ON_FAILURE = 'true'
        VIDEO_ON_FAILURE = 'true'
        TRACE_ON_FAILURE = 'true'
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

        stage('Create Environment File') {
            steps {
                bat '''
                    (
                        echo TEST_ENV=%TEST_ENV%
                        echo DEV_BASE_URL=%DEV_BASE_URL%
                        echo DEV_USERNAME=%DEV_USERNAME%
                        echo DEV_PASSWORD=%DEV_PASSWORD%
                        echo QA_BASE_URL=%QA_BASE_URL%
                        echo QA_USERNAME=%QA_USERNAME%
                        echo QA_PASSWORD=%QA_PASSWORD%
                        echo UAT_BASE_URL=%UAT_BASE_URL%
                        echo UAT_USERNAME=%UAT_USERNAME%
                        echo UAT_PASSWORD=%UAT_PASSWORD%
                        echo PROD_BASE_URL=%PROD_BASE_URL%
                        echo PROD_USERNAME=%PROD_USERNAME%
                        echo PROD_PASSWORD=%PROD_PASSWORD%
                        echo BROWSER=%BROWSER%
                        echo HEADLESS=%HEADLESS%
                        echo SLOW_MO=%SLOW_MO%
                        echo SCREENSHOT_ON_FAILURE=%SCREENSHOT_ON_FAILURE%
                        echo VIDEO_ON_FAILURE=%VIDEO_ON_FAILURE%
                        echo TRACE_ON_FAILURE=%TRACE_ON_FAILURE%
                    ) > .env

                    echo Environment configuration created for Jenkins.
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

        stage('Create Authentication State') {
            steps {
                bat '''
                    if exist auth rmdir /s /q auth
                    mkdir auth

                    .jenkins-venv\\Scripts\\python.exe -m pytest tests/login/test_auth_setup.py -v -s

                    if not exist auth\\auth_state.json (
                        echo ERROR: Authentication state was not created.
                        exit /b 1
                    )

                    echo Authentication state created successfully.
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

            bat '''
                if exist .env del /q .env
            '''
        }

        success {
            echo 'All Playwright-Pytest tests passed successfully.'
        }

        failure {
            echo 'Playwright-Pytest execution failed. Check the console output.'
        }
    }
}
