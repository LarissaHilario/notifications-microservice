pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'service-notifications'
        PORT_MAPPING = '8000:8000'
        CONTAINER_NAME = 'service-notifications-container' 
    }
    
    stages {
        stage('Stop All Containers') {
            steps {
                script {
                    sh 'docker stop $(docker ps -q)'
                    
                    sh 'docker rm $(docker ps -aq)'
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
