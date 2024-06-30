pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'service-notifications'
        PORT_MAPPING = '8000:8000'
        CONTAINER_NAME = 'service-notifications-container' 
        AWS_REGION = 'us-east-2'
        AWS_ACCESS_KEY_ID = env.AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY = env.AWS_SECRET_ACCESS_KEY
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
                    docker.run(env.SERVICE_NAME, "-e AWS_ACCESS_KEY_ID=${env.AWS_ACCESS_KEY_ID} \
                        -e AWS_SECRET_ACCESS_KEY=${env.AWS_SECRET_ACCESS_KEY} \
                        -e AWS_REGION=${env.AWS_REGION} \
                        -p 8000:8000")
                }
            }
        }
    }
}
