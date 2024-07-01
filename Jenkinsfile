pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'service-notifications'
        PORT_MAPPING = '8000:8000'
        CONTAINER_NAME = 'service-notifications-container'
        AWS_REGION = 'us-east-2'
        AWS_ACCESS_KEY_ID = "${env.AWS_ACCESS_KEY_ID}"
        AWS_SECRET_ACCESS_KEY = "${env.AWS_SECRET_ACCESS_KEY}"
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
                    def customImage = docker.build(DOCKER_IMAGE)
                    def runCommand = "docker run -d " +
                                     "-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} " +
                                     "-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} " +
                                     "-e AWS_REGION=${AWS_REGION} " +
                                     "-p ${PORT_MAPPING} " +
                                     "--name ${CONTAINER_NAME} "
                    
                    // Add the fetched environment variables to the Docker run command
                    envVars.each { key, value ->
                        runCommand += "-e ${key}=${value} "
                    }
                    
                    runCommand += "${DOCKER_IMAGE}"

                    // Run the Docker container with the environment variables
                    sh runCommand
                }
            }
        }
    }
}
