pipeline {
    agent { docker { image 'python:3.7.1' } }
//      environment {
//    WORKSPACE = "${env.WORKSPACE}"
//    }
    stages {
        stage('Checkout') {
          steps {
              checkout scm
                }
        }
        stage('build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                sh script:'''
                                #/bin/bash
                                echo "PATH is: $PATH"
                                  python --version
                                  python -m pip install --upgrade pip --user
                                  ls
                                  pip install --user -r requirements.txt
                                  export PATH="$WORKSPACE/.local/bin:$PATH"
                                    '''
                }
            }
        }
        stage('test') {
          steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh script:'''
          #!/bin/bash
          export PATH="$WORKSPACE/.local/bin:$PATH"
          echo "This is start $(pwd)"
          echo "This is $(pwd)"
          python jenkins_test.py

                  '''
         }
        }
      post {
        always {withEnv(["HOME=${env.WORKSPACE}"]) {
            junit allowEmptyResults: true, testResults: '**/test-reports/*.xml'
//            cleanWs()

        }
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