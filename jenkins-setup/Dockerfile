# Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# Pre-install plugins from plugins.txt
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Copy custom Groovy scripts for initialization
COPY scripts /usr/share/jenkins/ref/init.groovy.d/

# Set default user to root for advanced permissions
USER root

# Install Docker CLI inside Jenkins container (if needed)
RUN apt-get update && apt-get install -y docker.io && apt-get clean

# Switch back to Jenkins user
USER jenkins
