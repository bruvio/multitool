pipeline {
    agent { docker { image 'python:3.7.0' } }
    stages {
         stage ('Install_Requirements') {
            steps {
                sh '''
                    echo ${SHELL}
                    [ -d venv ] && rm -rf venv
                    #virtualenv --python=python2.7 venv
                    virtualenv venv
                    #. venv/bin/activate
                    export PATH=${VIRTUAL_ENV}/bin:${PATH}
                    pip install --upgrade pip
                    pip install -r requirements.txt -r dev-requirements.txt
                    make clean
                '''
            }
        }

        stage('test') {
      steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh script:'''
          #!/bin/bash
          echo "This is start $(pwd)"
          echo "This is $(pwd)"
          python tests/tests.py
#          python -m coverage run tests/tests.py
#          python -m coverage report tests/test.py
#          python -m coverage report -m *.py
#          python -m coverage html -d tests/test-reports/html *.py
                  '''
      }}
      post {
        always {withEnv(["HOME=${env.WORKSPACE}"]) {
          junit allowEmptyResults: true, testResults: '**/test-reports/*.xml'
            cleanWs()
        
      }} 
    }
}
}
}