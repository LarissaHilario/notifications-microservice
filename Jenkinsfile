pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'service-notifications'
        PORT_MAPPING = '8000:8000'
        CONTAINER_NAME = 'service-notifications-container'
        AWS_REGION = 'us-east-2'
        PARAMETER_PATH = '/90minutes/dev/services/notifications/'
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

        stage('Fetch Environment Variables') {
            steps {
                script {
                    // Define the list of environment variables to fetch
                    def envKeys = [
                        'DB.HOST_MYSQL',
                        'DB.PORT_MYSQL',
                        'DB.USER_MYSQL',
                        'DB.PASSWORD_MYSQL',
                        'DB.DATABASE_MYSQL',
                        'SNS_TOPIC_ARN',
                        'SNS_EMAIL_SUPPORT',
                        'SNS_PHONE_NUMBER_SUPPORT',
                        'RABBITMQ_HOST',
                        'RABBITMQ_PROTOCOL',
                        'RABBITMQ_USER',
                        'RABBITMQ_PASS',
                        'RABBITMQ_PORT'
                    ]

                    // Initialize envVars map
                    def envVars = [:]

                    // Fetch parameters from Parameter Store and store in envVars map
                    envKeys.each { key ->
                        def value = sh(script: "aws ssm get-parameter --name ${PARAMETER_PATH}${key} --with-decryption --query Parameter.Value --output text", returnStdout: true).trim()
                        envVars[key.replaceAll('\\.', '_')] = value
                    }

                    // Print out envVars for debugging
                    echo "Fetched Environment Variables:"
                    envVars.each { key, value ->
                        echo "${key}=${value}"
                    }

                    // Set environment variables in the current Jenkins environment
                    envVars.each { key, value ->
                        env."${key}" = "${value}"
                    }
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    def customImage = docker.build(env.DOCKER_IMAGE)
                    def runCommand = "docker run -d " +
                                     "-e AWS_ACCESS_KEY_ID=${env.AWS_ACCESS_KEY_ID} " +
                                     "-e AWS_SECRET_ACCESS_KEY=${env.AWS_SECRET_ACCESS_KEY} " +
                                     "-e AWS_REGION=${env.AWS_REGION} " +
                                     "-e DB_HOST_MYSQL=${env.DB_HOST_MYSQL} " +
                                     "-e DB_PORT_MYSQL=${env.DB_PORT_MYSQL} " +
                                     "-e DB_USER_MYSQL=${env.DB_USER_MYSQL} " +
                                     "-e DB_PASSWORD_MYSQL=${env.DB_PASSWORD_MYSQL} " +
                                     "-e DB_DATABASE_MYSQL=${env.DB_DATABASE_MYSQL} " +
                                     "-e SNS_TOPIC_ARN=${env.SNS_TOPIC_ARN} " +
                                     "-e SNS_EMAIL_SUPPORT=${env.SNS_EMAIL_SUPPORT} " +
                                     "-e SNS_PHONE_NUMBER_SUPPORT=${env.SNS_PHONE_NUMBER_SUPPORT} " +
                                     "-e RABBITMQ_HOST=${env.RABBITMQ_HOST} " +
                                     "-e RABBITMQ_PROTOCOL=${env.RABBITMQ_PROTOCOL} " +
                                     "-e RABBITMQ_USER=${env.RABBITMQ_USER} " +
                                     "-e RABBITMQ_PASS=${env.RABBITMQ_PASS} " +
                                     "-e RABBITMQ_PORT=${env.RABBITMQ_PORT} " +
                                     "-p ${env.PORT_MAPPING} " +
                                     "--name ${env.CONTAINER_NAME} " +
                                     "${env.DOCKER_IMAGE}"

                    // Run the Docker container with the environment variables
                    sh runCommand
                }
            }
        }
    }
}
