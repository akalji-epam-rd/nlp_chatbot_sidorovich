pipeline {
    agent {
        node {
            customWorkspace '/home/centos/rasa/innkeeper_rasabot'
        }
    }
    environment {
        projectFolder = "/home/centos/rasa/"
        gitRepoName = "innkeeper_rasabot"
        scmPath = "${projectFolder}/${gitRepoName}"
      
        logFolder = "${projectFolder}/logs"
        varLogPath = "${logFolder}/runtime.log"
        
        venvBin = "${scmPath}/venv/bin"
        modules = "${scmPath}/requirements.txt"
        
        user = "centos"
        port_rasa = "5005"
		    port_actions = "5055"
		
    }
    options {
        skipDefaultCheckout true
    }
    stages {
        stage("checkout") {
            steps {
                checkout scm
            }
        }
        stage("Kill Previous") {
            steps {
                sh "sudo lsof -t -i:${port_rasa} | sudo xargs -r kill -9"
				sh "sudo lsof -t -i:${port_actions} | sudo xargs -r kill -9"
            }
        }
        stage("Venv") {
            steps {
                sh "sudo mkdir -p ${logFolder}"
                sh "sudo chown ${user}:${user} ${logFolder}"
                
                sh "sudo virtualenv venv --python=python3"
                sh "sudo ${venvBin}/pip3.6 install -r ${modules}"
            }
        }
		stage("NLU train") {
            steps {
                sh "sudo python3.6 -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose"
            }
        }
		stage("Core train") {
            steps {
                sh "sudo python3.6 -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue"
            }
        }
		stage("Start actions") {
            steps {
                sh "sudo python3.6 -m rasa_core_sdk.endpoint --actions actions --port ${port_actions} &"
            }
        }
		stage("Start bot") {
            steps {
                sh "sudo python3.6 -m rasa_core.run -d models/dialogue -u models/current/nlu --port ${port_rasa} --endpoints endpoints.yml --credentials credentials.yml &"
            }
        }
    }
}
