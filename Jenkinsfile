pipeline {
    agent { docker { image 'python:3.7.0' } }
    stages {
        stage('build') {
            steps {
                withEnv(["HOME=${env.WORKSPACE}"]) {
                                    sh 'python --version'

                                    sh 'pip install --user -r requirements.txt'
            }
        }
    }
        stage('test') {
      steps {withEnv(["HOME=${env.WORKSPACE}"]) {
                sh script:'''
          #!/bin/bash
          echo "This is start $(pwd)"
          echo "This is $(pwd)"
          python tests/test.py
#          python -m coverage run tests/test.py
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