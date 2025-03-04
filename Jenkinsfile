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

        stage('Setup Python and Install Requirements Run REST API Web') {
            steps {
                    script {
                                // Install Python dependencies
                                sh """
                                    pwd
                                    ls
                                    python3 -m venv /var/snap/jenkins/4817/workspace/test-multi-branch-pipeline_main
                                    bash -c 'source /var/snap/jenkins/4817/workspace/test-multi-branch-pipeline_main/bin/activate && python3 -m pip install -r requirements.txt && python3 --version && uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4 &'
                                """
                            }
                    }
        }

        stage('Test') {
            steps {
                echo "Running tests for commit ${COMMIT_ID}"
                sh 'uname' // Replace with your test command
                sh  """
                    echo "Waiting for the server to start..."
                    sleep 10
                    echo "Checking if the server is running..."
                    netstat -tulnp | grep 8000 || (echo "Server is not running!" && exit 1)
                    curl http://localhost:8000/get_hostname || (echo "Failed to reach API!" && exit 1)
                    curl http://localhost:8000/get_ror
                    curl http://localhost:8000/list_sut
                    """
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