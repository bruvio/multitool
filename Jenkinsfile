pipeline {
    agent { docker { image 'python:3.7.1' } }
      environment {
    WORKSPACE = "${env.WORKSPACE}"
    PATH = "${env.PATH}"
    }
    stages {
        stage('Checkout') {
          steps {
              checkout scm
                }
        }
        stage('build') {
            steps {

                sh script:'''
                                #/bin/bash
                                echo "WORKSPACE is: $WORKSPACE"
                                echo "PATH is: $PATH"
                                  python --version
                                  python -m pip install --upgrade pip --user
                                  ls
                                  pip install --user -r requirements.txt
                                    '''

            }
        }
        stage('test') {
          steps {
                sh script:'''
          #!/bin/bash
          echo "This is start $(pwd)"
          echo "This is $(pwd)"
          python jenkins_test.py

                  '''

        }
      post {
        always {
            junit allowEmptyResults: true, testResults: '**/test-reports/*.xml'
//            cleanWs()
        
        
        } 
      }
}
}
}
//          python tests/tests.py
//          python -m coverage run tests/tests.py
//          python -m coverage report tests/tests.py
//          python -m coverage report -m *.py
//          python -m coverage html -d tests/test-reports/html *.py