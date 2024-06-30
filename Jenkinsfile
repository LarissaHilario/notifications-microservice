pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'service-notifications'
        PORT_MAPPING = '8000:8000'
        CONTAINER_NAME = 'service-notifications-container' 
    }
    
    stages {
        stage('Stop Container and Remove') {
            steps {
                script {
                    sh "docker stop ${CONTAINER_NAME}"
                    
                    sh "docker rm ${CONTAINER_NAME}"
                }
            }
        }
        
        stage('Build and Deploy') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                    sh "docker run -d -p ${PORT_MAPPING} --name ${CONTAINER_NAME} ${DOCKER_IMAGE}"
                }
            }
        }
    }
}
