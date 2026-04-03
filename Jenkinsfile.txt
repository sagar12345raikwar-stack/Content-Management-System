pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'staging', 'prod'], description: 'Select Environment')
    }

    environment {
        CACHE = "cache"
    }

    stages {

        stage('Setup Cache') {
            steps {
                script {
                    if (!fileExists(CACHE)) {
                        sh "mkdir ${CACHE}"
                        echo "Cache created"
                    } else {
                        echo "Using cached dependencies"
                    }
                }
            }
        }

        stage('Build & Test') {
            steps {
                retry(2) {
                    sh '''
                    echo "Building application..."
                    sleep 1

                    echo "Running tests..."
                    sleep 1

                    mkdir -p output
                    echo "App build file" > output/app.txt

                    tar -czf app.tar.gz output
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                expression { params.ENV != "" }
            }
            steps {
                echo "Deploying to ${params.ENV}"

                sh '''
                echo "Using artifact: app.tar.gz"
                echo "Deployment successful!"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline Success"
        }
        failure {
            echo "❌ Pipeline Failed"
        }
    }
}
