pipeline {
    agent { docker { image 'python:3.7.1' } }
      environment {
    WORKSPACE = "${env.WORKSPACE}"
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

                                  python --version
                                  python -m pip install --upgrade pip --user
                                  ls
                                  pip install --user -r requirements.txt
                                  export PATH="$WORKSPACE/.local/bin:$PATH"
                                    '''

            }
        }
        stage('test') {
          steps {
                sh script:'''
          #!/bin/bash
          echo "WORKSPACE is: $WORKSPACE"
          export PATH="$WORKSPACE/.local/bin:$PATH"
          echo "we are in $(pwd)"
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