import jenkins.model.*
import hudson.util.Secret
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.*

def githubCredentialsId = 'github-token'
def githubToken = "Y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" // Replace with your GitHub token

def credentials = new StringCredentialsImpl(
    CredentialsScope.GLOBAL,
    githubCredentialsId,
    "GitHub Token",
    Secret.fromString(githubToken)
)

SystemCredentialsProvider.getInstance().getStore().addCredentials(Domain.global(), credentials)
