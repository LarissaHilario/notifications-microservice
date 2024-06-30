pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'service-notifications'
        PORT_MAPPING = '8000:8000'
        CONTAINER_NAME = 'service-notifications-container' 
    }
    stages {
        stage('Build') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        stage('Deploy') {
            steps {
                script {

                    def runningContainerId = sh(script: "docker ps -q --filter 'ancestor=${DOCKER_IMAGE}'", returnStdout: true).trim()
                    
                    if (runningContainerId) {
                        sh "docker stop ${runningContainerId}"
                    } else {
                        echo "No hay contenedor en ejecución con la imagen ${DOCKER_IMAGE}"
                    }
                    
                    sh "docker rm ${runningContainerId}"

                    docker.image(DOCKER_IMAGE).run("-p ${PORT_MAPPING} --name ${CONTAINER_NAME} -d")
                }
            }
        }
    }
}
