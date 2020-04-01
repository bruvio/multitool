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
                  steps {
                sh '''pip install --upgrade pip
                      pip install -r requirements.txt
                    '''
            }
    }
    stage('Test environment') {
            steps {
                sh '''
                      pip list
                      which pip
                      which python
                    '''
            }
        }
    stage('test') {
      steps {
        sh '''
            echo "This is start $(pwd)"
            python tests/test.py
        '''
      }
    }
  }
}