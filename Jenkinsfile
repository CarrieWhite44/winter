pipeline {

    agent any

    environment{
        IMAGE_NAME = "tprff2301/winter-app"
        IMAGE_TAG = ${BUILD_NUMBER}
    }

    stages{
        stage('Build'){
            steps{
                sh  ''' docker build \
                    -t $IMAGE_NAME:$IMAGE_TAG \
                    .
                '''
            }
        }

        stage('Push'){
            steps{
                withCredentials([
                    usernamePassword(
                        credentialsId: 'winter-docker-token-id',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ])
                {
                    sh '''
                    echo $DOCKER_PASS | docker login \
                    -u $DOCKER_USER \
                    --password-stdin

                    docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy'){
            steps{
                withCredentials([
                    file(
                        credentialsId: 'kubeconfig',
                        variable: 'KUBECONFIG'
                    )
                ]) {
                    sh '''
                    kubectl set image deployment/winter-app \
                    winter-app=$IMAGE_NAME:$IMAGE_TAGE

                    kubectl rollout status deployment/winter-app
                    '''
                }
            }
        }
    }

    post{
        always{
            sh '''
            docker image prune -af || true '''
        }
    }

}