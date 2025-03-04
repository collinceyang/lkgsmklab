pipeline {
    agent any

    environment {
        COMMIT_ID = "${GIT_COMMIT}" // Get the latest commit SHA
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out commit: ${COMMIT_ID} from branch: ${BRANCH_NAME}"
                }
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Building commit ${COMMIT_ID}"
                sh 'lsb_release -a' // Replace with your build command
            }
        }

        stage('Test') {
            steps {
                echo "Running tests for commit ${COMMIT_ID}"
                sh 'uname' // Replace with your test command
            }
        }

        stage('Code Linting') {
            steps {
                echo "Checking code quality for commit ${COMMIT_ID}"
                sh 'hostname' // Replace with your lint command
            }
        }

        stage('Deploy Preview (Optional)') {
            steps {
                echo "Deploying preview for commit ${COMMIT_ID} from ${BRANCH_NAME}"
                sh 'ifconfig' // Replace with your preview deployment command
            }
        }
    }

    post {
        always {
            echo "Pipeline completed for commit ${COMMIT_ID}"
        }
        success {
            echo "Build succeeded for commit ${COMMIT_ID}"
        }
        failure {
            echo "Build failed for commit ${COMMIT_ID}"
        }
    }
}