pipeline {
      agent { docker { image 'python:3.7.1' } }
    options {
        skipDefaultCheckout(true)
        // Keep the 10 most recent builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
  stages {
    stage('Build environment') {
                  steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh '''pip install --upgrade pip
                      pip install -r requirements.txt
                    '''
            }}
    }
    stage('Test environment') {
            steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh '''
                      pip list
                      which pip
                      which python
                    '''
            }}
        }
    stage('test') {
      steps {withEnv(["HOME=${env.WORKSPACE}"]) {
        sh '''
            echo "This is start $(pwd)"

        '''
      }}
      post {
        always {
          
            cleanWs()
        
        }
      }  
    } 
  }
}
