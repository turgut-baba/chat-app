pipeline {
    agent any  // Runs on any available agent

    environment {
        VIRTUAL_ENV = "${WORKSPACE}/venv"  // Define virtual environment path
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    // Install Python and dependencies
                    sh 'python3 -m venv $VIRTUAL_ENV'
                    sh 'source $VIRTUAL_ENV/bin/activate && pip install --upgrade pip'
                    sh 'source $VIRTUAL_ENV/bin/activate && pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run pytest with WebSocket server
                    sh 'source $VIRTUAL_ENV/bin/activate && pytest --maxfail=1 --disable-warnings'
                }
            }
        }
    }

    post {
        always {
            script {
                // Cleanup workspace
                sh 'rm -rf $VIRTUAL_ENV'
            }
        }
        success {
            echo 'Tests passed successfully!'
        }
        failure {
            echo 'Tests failed. Check logs for details.'
        }
    }
}
