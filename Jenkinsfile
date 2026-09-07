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

        stage('Run Tests') {
            steps {
                catchError(
                    buildResult: 'FAILURE',
                    stageResult: 'FAILURE'
                ) {
                    bat '''
                        if not exist test-results mkdir test-results

                        .jenkins-venv\\Scripts\\python.exe -m pytest tests/login tests/buzz tests/vacancy -v -s --junitxml=test-results\\pytest-results.xml
                    '''
                }
            }
        }

        stage('Test Summary') {
            steps {
                bat '''
                    echo.
                    echo ==========================================
                    echo       PLAYWRIGHT TEST SUMMARY
                    echo ==========================================

                    powershell -NoProfile -Command "$xml = [xml](Get-Content 'test-results\\pytest-results.xml'); $testCases = @($xml.testsuites.testsuite.testcase); $loginTests = @($testCases | Where-Object { $_.classname -match 'tests[\\\\/.]login' }); $buzzTests = @($testCases | Where-Object { $_.classname -match 'tests[\\\\/.]buzz' }); $vacancyTests = @($testCases | Where-Object { $_.classname -match 'tests[\\\\/.]vacancy' }); $loginFailed = @($loginTests | Where-Object { $_.failure -or $_.error }).Count; $buzzFailed = @($buzzTests | Where-Object { $_.failure -or $_.error }).Count; $vacancyFailed = @($vacancyTests | Where-Object { $_.failure -or $_.error }).Count; $loginSkipped = @($loginTests | Where-Object { $_.skipped }).Count; $buzzSkipped = @($buzzTests | Where-Object { $_.skipped }).Count; $vacancySkipped = @($vacancyTests | Where-Object { $_.skipped }).Count; if ($loginTests.Count -eq 0) { $loginStatus = 'NOT RUN' } elseif ($loginFailed -gt 0) { $loginStatus = 'FAILED' } elseif ($loginSkipped -eq $loginTests.Count) { $loginStatus = 'SKIPPED' } else { $loginStatus = 'PASSED' }; if ($buzzTests.Count -eq 0) { $buzzStatus = 'NOT RUN' } elseif ($buzzFailed -gt 0) { $buzzStatus = 'FAILED' } elseif ($buzzSkipped -eq $buzzTests.Count) { $buzzStatus = 'SKIPPED' } else { $buzzStatus = 'PASSED' }; if ($vacancyTests.Count -eq 0) { $vacancyStatus = 'NOT RUN' } elseif ($vacancyFailed -gt 0) { $vacancyStatus = 'FAILED' } elseif ($vacancySkipped -eq $vacancyTests.Count) { $vacancyStatus = 'SKIPPED' } else { $vacancyStatus = 'PASSED' }; Write-Host ('Login       -> ' + $loginStatus); Write-Host ('Buzz        -> ' + $buzzStatus); Write-Host ('Vacancy     -> ' + $vacancyStatus); Write-Host ''; Write-Host '=========================================='; Write-Host '       PLAYWRIGHT TEST SUMMARY'; Write-Host '=========================================='; $statuses = @($loginStatus, $buzzStatus, $vacancyStatus); $passed = @($statuses | Where-Object { $_ -eq 'PASSED' }).Count; $failed = @($statuses | Where-Object { $_ -eq 'FAILED' }).Count; $skipped = @($statuses | Where-Object { $_ -eq 'SKIPPED' }).Count; Write-Host 'Total Tests : 3'; Write-Host ('Passed      : ' + $passed); Write-Host ('Failed      : ' + $failed); Write-Host ('Skipped     : ' + $skipped); Write-Host '=========================================='"
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
            echo 'All Playwright-Pytest test areas passed successfully.'
        }

        failure {
            echo 'Playwright-Pytest execution failed. Check the console output.'
        }
    }
}
