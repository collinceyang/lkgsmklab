pipeline {
    agent any

    environment {
        COMMIT_ID = "${GIT_COMMIT}" // Get the latest commit SHA
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()  // Deletes previous workspace files
                script {
                    echo "Workspace cleaned successfully."
                }
            }
        }

        stage('Get Current Path') {
            steps {
                script {
                    def workspacePath = env.WORKSPACE  // Get Jenkins workspace path
                    echo "Current workspace path: ${workspacePath}"
                }
            }
        }
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
                echo "Building the project in: ${env.WORKSPACE}"
                echo "Building commit ${COMMIT_ID}"
                sh 'lsb_release -a' // Replace with your build command
            }
        }

        stage('Setup Python and Install Requirements Run REST API Web') {
            steps {
                    script {
                                // Install Python dependencies
                                sh """
                                    #!/bin/bash
                                    pwd
                                    ls
                                    python3 -m venv ${env.WORKSPACE}
                                    chmod +x  ${env.WORKSPACE}/bin/activate
                                    ${env.WORKSPACE}/bin/pip install -r requirements.txt  && ${env.WORKSPACE}/bin/python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4&
                                """
                            }
                    }
        }

        // stage('Test - Curl API') {
        //     steps {
        //         echo "Running tests for commit ${COMMIT_ID}"
        //         sh 'uname' // Replace with your test command
        //         sh  """
        //             echo "Waiting for the server to start..."
        //             sleep 10
        //             echo "Checking if the server is running..."
        //             netstat -tulnp | grep 8000 || (echo "Server is not running!" && exit 1)
        //             curl http://localhost:8000/get_hostname || (echo "Failed to reach API!" && exit 1)
        //             curl http://localhost:8000/get_ror
        //             curl http://localhost:8000/list_sut
        //             """
        //     }
        // }

        stage('Test - PyTest') {
            steps {
                echo "Running pytest tests for commit ${COMMIT_ID}"
                sh """
                    . ${env.WORKSPACE}/bin/python3 -m pytest 
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
                sh curl http://localhost:8000/list_sut
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