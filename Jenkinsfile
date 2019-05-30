import groovy.json.JsonSlurper

node {
	stage ('checkout') {
		checkout scm
	}
	stage('checksum') {
		md5sum_from_file = sh(returnStdout: true, script: "cat MD5Sum")
		md5sum = sh(returnStdout: true, script: "md5sum forcast_collector.py | awk '{print \$1} '")
		script {
			echo md5sum
			echo md5sum_from_file
			if (md5sum != md5sum_from_file) {
				buildStatus = "FAILURE"
				error("Checksum failed")
			} 
		}
	}
	stage('run script') {
		sh 'python3 forcast_collector.py'
	}
	stage('validate output') {
			
		try {
			def validation = readJSON file: "forcast_data.json"

		}
		catch (Exception err) {
			echo err.toString()
			error("JSON validation failed")
		}
	}		
}
