pipeline {
    agent { docker { image 'python:3.7.1' } }

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
                                  pip install virtualenv --verbose

                                  # Get an unique venv folder to using *inside* workspace
                                  VENV="$HOME/.local"

                                  # Initialize new venv
                                  echo "virtualenv $VENV"
                                  virtualenv "$VENV"

                                  # Update pip
                                  echo "activate virtualenv"
                                  source "$VENV/bin/activate"


                                  pip install -r requirements.txt
                                    '''
                }
            }
        }
        stage('test') {
          steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh script:'''
          #!/bin/bash
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