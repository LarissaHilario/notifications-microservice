pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'service-notifications'
        PORT_MAPPING = '8000:8000'
        CONTAINER_NAME = 'service-notifications-container'
        AWS_REGION = 'us-east-2'
        AWS_ACCESS_KEY_ID = "${env.AWS_ACCESS_KEY_ID}"
        AWS_SECRET_ACCESS_KEY = "${env.AWS_SECRET_ACCESS_KEY}"
    }

    stages {
        stage('Stop Container and Remove') {
            steps {
                script {
                    def containerExists = sh(script: "docker ps -a -q -f name=${CONTAINER_NAME}", returnStdout: true).trim()
                    if (containerExists) {
                        sh "docker stop ${CONTAINER_NAME}"
                        sh "docker rm ${CONTAINER_NAME}"
                    } else {
                        echo "Container ${CONTAINER_NAME} does not exist."
                    }
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                   def customImage = docker.build(DOCKER_IMAGE)
                   
                    docker run -d -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                        -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                        -e AWS_REGION=${AWS_REGION} \
                        -p ${PORT_MAPPING} \
                        --name ${CONTAINER_NAME} ${DOCKER_IMAGE}
                }
            }
        }
    }
}
