FROM --platform=linux/amd64 ubuntu:20.04

# To make it easier for build and release pipelines to run apt-get,
# configure apt to not require confirmation (assume the -y argument by default)
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "APT::Get::Assume-Yes \"true\";" > /etc/apt/apt.conf.d/90assumeyes

# Define ENVs for Localization/Globalization
ENV LANG=en_US.UTF-8

# Install tooling
RUN apt-get update && apt-get install -y \
    less \
    npm \
    wget \
    nodejs \
    locales \
    gss-ntlmssp \
    openssh-client \
    curl \
    jq \
    git \
    netcat \
    apt-transport-https \
    lsb-release \
    gnupg \
    build-essential \
    python-all \
    rlwrap  \
    vim  \
    zip \
    unzip \
    iputils-ping \
    software-properties-common \
    sudo \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install boto3
RUN pip3 install boto3

# copy over the start.py script
COPY start.py start.py

# make the script executable
RUN chmod +x start.py

# Updates and cleanup
RUN apt-get update -yq \
    && apt-get upgrade -yq \
    && rm -rf /var/lib/apt/lists/*

# set the entrypoint to the start.py script
ENTRYPOINT ["python3","./start.py"]
