pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'service-notifications'
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
                    docker.image(DOCKER_IMAGE).run('-p 8000:8000')
                }
            }
        }
    }
}