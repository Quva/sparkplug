registry = "extranet.quva.fi:57104"
repository = "sparkplug"

node {

    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        image = "${registry}/${repository}:latest"
        sh "docker build --tag $image ."
    }

    stage('Push') {
        branchImage = "${registry}/${repository}:latest"
        sh "docker push $image && docker tag $image $branchImage && docker push $branchImage"
    }
}
