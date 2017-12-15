@Library('Pipeline Libraries@pschami') _
properties(getBuildProperties())

pipeline {
    parameters {
        string(name: 'releaseVersion', defaultValue: '1')
        string(name: 'majorVersion', defaultValue: '0')
        string(name: 'minorVersion', defaultValue: '0')
        string(name: 'gitVersion', defaultValue: '1')
    }
    agent {
        node {
            label 'maven-builder'
            customWorkspace "workspace/${env.JOB_NAME}"
        }
    }
    environment {
        GITHUB_TOKEN = credentials('git-02')
    }
    options {
        skipDefaultCheckout()
        timestamps()
    }
    tools {
        maven 'linux-maven-3.3.9'
        jdk 'linux-jdk1.8.0_102'
    }
    stages {
        stage('Checkout') {
            steps {
                doCheckout()
            }
        }
        stage('NexB Scan') {
            steps {
                doNexbScanning()
            }
        }
        stage('Build') {
            steps {
                sh "echo create_rpms"
            }
        }
        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: '**/*.rpm', fingerprint: false
            }
        }
        stage('Upload to Repo') {
            steps {
                uploadArtifactsToArtifactory("master|rpm-packaging|q3stable")
            }
        }
        /*
        stage('SonarQube Analysis') {
            steps {
                doSonarAnalysis()
            }
        }
        */
        /*
        stage('Third Party Audit') {
            steps {
                doThirdPartyAudit()
            }
        }
        */
        stage('PasswordScan') {
            steps {
                doPwScan()
            }
        }
         stage('BadgeCheck') {
            steps {
                doBadgeCheck()
            }
        }
         stage('CheckPom') {
            steps {
                doCheckPom()
            }
        }
        stage('Github Release') {
            steps {
                githubRelease()
            }
        }
    }
    post {
        always {
            cleanWorkspace()   
        }
        success {
            successEmail()
        }
        failure {
            failureEmail()
        }
    }
}
