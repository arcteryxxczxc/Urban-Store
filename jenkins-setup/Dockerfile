# Use the official Jenkins LTS image as the base
FROM jenkins/jenkins:lts

# Set default user to root for advanced permissions
USER root

# Install Docker CLI
RUN apt-get update && apt-get install -y \
    docker.io \
    curl \
    apt-transport-https \
    ca-certificates \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && apt-get update && apt-get install -y docker-ce-cli \
    && apt-get clean

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Switch back to Jenkins user
USER jenkins

# Pre-install plugins from plugins.txt
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Copy custom Groovy scripts for initialization
COPY scripts /usr/share/jenkins/ref/init.groovy.d/
