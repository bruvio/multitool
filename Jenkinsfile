pipeline {
      agent { docker { image 'python:3.7.1' } }
    options {
        skipDefaultCheckout(true)
        // Keep the 10 most recent builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build environment') {
                  steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                                    sh 'python --version'
                                    sh 'python -m pip install --upgrade pip --user'
                                    sh 'ls'
                                    sh 'pip install --user -r requirements.txt --user'
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


//script {
//                    sh 'virtualenv env -p python3.5'
//                    sh '. env/bin/activate'
//                    sh "env/bin/pip install -r requirements/private.txt"
//                    sh "env/bin/pip install -r requirements/${env.ENVIRONMENT}.txt"
//                    sh 'env/bin/python3.5 manage.py test --pattern="test_*.py'
//                }