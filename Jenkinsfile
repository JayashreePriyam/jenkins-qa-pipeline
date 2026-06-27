pipeline {
    agent any
    parameters {
        choice(name: 'TEST_ENV', choices: ['staging', 'dev', 'production'], description: 'Environment')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox', 'edge'], description: 'Browser')
        choice(name: 'TEST_SUITE', choices: ['all', 'login', 'payment', 'api'], description: 'Test suite')
    }
    environment {
        TEST_ENV = "${params.TEST_ENV}"
        BROWSER = "${params.BROWSER}"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                sh 'python3 -m pip install --user -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    def testPath = "tests/"
                    if (params.TEST_SUITE == 'login') {
                        testPath = "tests/test_sample.py::TestLoginPage"
                    } else if (params.TEST_SUITE == 'payment') {
                        testPath = "tests/test_sample.py::TestPaymentValidation"
                    } else if (params.TEST_SUITE == 'api') {
                        testPath = "tests/test_sample.py::TestAPIHealth"
                    }
                    sh "python3 -m pytest ${testPath} -v --tb=short --junitxml=reports/test-results.xml -s"
                }
            }
        }
        stage('Generate Report') {
            steps {
                junit allowEmptyResults: true, testResults: 'reports/test-results.xml'
            }
        }
    }
    post {
        success { echo "All tests PASSED on ${TEST_ENV}!" }
        failure { echo "Tests FAILED on ${TEST_ENV}!" }
        always { echo "Done. Env: ${TEST_ENV}, Browser: ${BROWSER}" }
    }
}
