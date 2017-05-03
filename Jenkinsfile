registry = "extranet.quva.fi:57104"
repository = "sparkplug"

// This controls which build is triggered
deploymentMap = [
  "dev": "../Flow/feature-dab"
]

node {

  def status = 'STARTED'

  try {

    stage('Checkout') {
      notify(status)
      checkout scm
    }

    stage('Build') {
      tag = sh(returnStdout: true, script: "git describe").trim()
      image = "${registry}/${repository}:${tag}"

      sh "docker build --tag $image ."
    }

    stage('Test') {
        wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'xterm']) {
          sh "docker run --rm $image make test"
      }
    }

    stage('Push') {
      branchImage = "${registry}/${repository}:${env.BRANCH_NAME}"
      sh "docker push $image && docker tag $image $branchImage && docker push $branchImage"
    }

    if (deploymentMap[env.BRANCH_NAME]) {
      stage('Deploy') {
        build job: deploymentMap[env.BRANCH_NAME], wait: false
      }
    } else {
      echo "No auto-deployment configured for this branch"
    }

    status = "SUCCEEDED"

  } catch (e) {
    status = "FAILED"
  } finally {
    notify(status)
  }
}

def notify(String status) {

  def color = "#000000"

  if (status == "STARTED" ) {
    color = "#FFFF00"
  } else if ( status == "SUCCEEDED" ) {
    color = "#00FF00"
  } else if ( status == "FAILED" ) {
    color = "#FF0000"
  }

  def message = "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})"

  slackSend(color: color, message: message)

}
