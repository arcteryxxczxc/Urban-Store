import jenkins.model.*
import hudson.plugins.git.*
import org.jenkinsci.plugins.workflow.cps.*

// Add GitHub credentials
def githubCredentialsId = 'github-token'
def githubToken = "YOUR_GITHUB_TOKEN" // Replace with your GitHub token
def credentials = new org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl(
    hudson.util.Secret.fromString(githubToken), githubCredentialsId, null, null
)
Jenkins.instance.getExtensionList(
    com.cloudbees.plugins.credentials.CredentialsProvider.class
)[0].addCredentials(
    com.cloudbees.plugins.credentials.domains.Domain.global(),
    credentials
)

// Create a pipeline job
def jobName = "GitHub_Pipeline"
def githubRepo = "https://github.com/USERNAME/REPOSITORY.git" // Replace with your GitHub repository

def job = Jenkins.instance.createProject(org.jenkinsci.plugins.workflow.job.WorkflowJob, jobName)
def script = """
pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: '${githubRepo}', credentialsId: '${githubCredentialsId}'
            }
        }
        stage('Build') {
            steps {
                sh 'echo Building...'
            }
        }
        stage('Test') {
            steps {
                sh 'echo Testing...'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo Deploying...'
            }
        }
    }
}
"""
job.definition = new CpsFlowDefinition(script, true)

// Save Jenkins configuration
Jenkins.instance.save()
