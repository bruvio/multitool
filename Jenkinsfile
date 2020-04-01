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
                                    sh 'python --version'
//                                    sh 'python -m pip install --upgrade pip'
//                                    sh 'pip install --user -r requirements.txt'
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
    }
  }
}


