    node {
        stage ('checkout') {
            checkout scm
        }
		stage('checksum') {
			md5sum_from_file = sh(returnStdout: true, script: "MD5Sum | awk '{print $1}'")
			md5sum = sh(returnStdout: true, script: "md5sum forcast_collector.py")
			script {
				if (md5sum != md5sum_from_file) {
					buildStatus = "FAILURE"
					error("Checksum failed")
				} 
			}
		}
		stage('run script') {
			sh 'python forcast_collector.py'
		}
		stage('validate output') {
			def inputFile = new File("forcast_data.json")
			
			try {
				def InputJSON = new JsonSlurper().parseText(inputFile.text)
				buildStatus = "SUCCESS"
			}
			catch (Exception err) {
				buildStatus = "FAILURE"
				error("JSON validation failed")
			}
		}		
	}
