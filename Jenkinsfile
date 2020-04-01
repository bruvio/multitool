pipeline {
      agent { docker { image 'python:3.7.1' args '--user 0:0'} }
    options {
        skipDefaultCheckout(true)
        // Keep the 10 most recent builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
  stages {
    stage('Build environment') {
                  steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh '''python -m pip install --user --upgrade pip
                      python -m pip install -r requirements.txt --user
                   '''
            }}
    }
    stage('Test environment') {
            steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh '''
                      python -m pip list
                      which pip
                      which python
                      python --version
                    '''
            }}
        }
    stage('test') {
      steps {withEnv(["HOME=${env.WORKSPACE}"]) {
        sh '''
            echo "This is start $(pwd)"
            python jenkins_test.py

        '''
      }}
      post {
        always {
          
            cleanup { cleanWs() }
        
        }
      }  
    } 
  }
}


