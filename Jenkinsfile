pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/arcteryxxczxc/Urban-Store.git' // URL репозитория
        CREDENTIALS_ID = 'github-ssh-key-2' // ID учётных данных в Jenkins
    }

    stages {
        stage('Clone') {
            steps {
                echo 'Starting repository clone...' // Лог перед началом клонирования
                git branch: 'main', url: "${REPO_URL}", credentialsId: "${CREDENTIALS_ID}"
                echo 'Repository cloned successfully!' // Лог после успешного клонирования
            }
        }

        stage('Build') {
            steps {
                echo 'Starting Docker build...' // Лог перед началом сборки
                sh 'docker-compose build'
                echo 'Docker build completed!' // Лог после успешной сборки
            }
        }

        stage('Test') {
            steps {
                echo 'Starting tests...' // Лог перед тестами
                sh 'pytest tests/' // Убедитесь, что тесты работают
                echo 'Tests completed successfully!' // Лог после успешного завершения тестов
            }
        }

        stage('Deploy') {
            steps {
                echo 'Starting deployment...' // Лог перед развертыванием
                sh 'docker-compose up -d'
                echo 'Application deployed successfully!' // Лог после успешного развертывания
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished!' // Финальный лог
        }
        failure {
            echo 'Pipeline failed! Check the logs above for more details.' // Лог при ошибке
        }
    }
}
