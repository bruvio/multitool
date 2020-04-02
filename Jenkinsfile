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

                sh script:'''
                                #/bin/bash
                                  pip install virtualenv --user
                                  python -m venv python
                                  # Get an unique venv folder to using *inside* workspace
                                  VENV=".local"

                                  # Initialize new venv
                                  virtualenv "$VENV"

                                  # Update pip
                                  PS1="${PS1:-}" source "$VENV/bin/activate"


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