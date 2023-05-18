# ubuntu:22.04
FROM ubuntu@sha256:67211c14fa74f070d27cc59d69a7fa9aeff8e28ea118ef3babc295a0428a6d21 AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV CLANG_VERSION 15

# Note: If the host user has different UID:GID and it causes trouble, either build this image
# with correct UID:GID or if more people run into this we change UID:GID of `user` in the
# entrypoint script.
ARG UID=1000
ARG GID=1000
ARG ZSDK_VERSION=0.16.0
ARG WGET_ARGS="-q --show-progress --progress=bar:force:noscroll --no-check-certificate"

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install --no-install-recommends -y \
        apt-utils \
        git \
        cmake \
        ninja-build \
        gperf \
        ccache \
        dfu-util \
        device-tree-compiler \
        wget \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-tk \
        python3-wheel \
        xz-utils \
        file \
        make \
        gcc \
        gcc-multilib \
        g++-multilib \
        libsdl2-dev \
        libmagic1 \
        sudo \
        locales

# Install the clang-format
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
     clang-format-$CLANG_VERSION clang-tidy-$CLANG_VERSION 


# Initialise system locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Install Python dependencies
RUN python3 -m pip install -U pip && \
    pip3 install -U wheel setuptools && \
    pip3 install \
        -r https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/zephyr-v3.3.0/scripts/requirements.txt \
        -r https://raw.githubusercontent.com/nasa/fprime/v3.2.0/requirements.txt \
        west && \
    pip3 check

# Create 'user' account
RUN groupadd -g $GID -o user

RUN useradd -u $UID -m -g user -G plugdev user \
    && echo 'user ALL = NOPASSWD: ALL' > /etc/sudoers.d/user \
    && chmod 0440 /etc/sudoers.d/user

# Adjust 'user' home directory permissions
RUN chown -R user:user /home/user

# Install Zephyr SDK
RUN mkdir -p /opt/toolchains && \
    cd /opt/toolchains && \
    wget ${WGET_ARGS} https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v${ZSDK_VERSION}/zephyr-sdk-${ZSDK_VERSION}_linux-x86_64.tar.xz && \
    wget -O - https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v${ZSDK_VERSION}/sha256.sum | shasum --check --ignore-missing && \
    tar xvf zephyr-sdk-${ZSDK_VERSION}_linux-x86_64.tar.xz && \
    zephyr-sdk-${ZSDK_VERSION}/setup.sh -t all -h -c && \
    rm zephyr-sdk-${ZSDK_VERSION}_linux-x86_64.tar.xz

# Run the Zephyr SDK setup script as 'user' in order to ensure that the
# `Zephyr-sdk` CMake package is located in the package registry under the
# user's home directory.
USER user

RUN sudo -E -- bash -c ' \
    /opt/toolchains/zephyr-sdk-${ZSDK_VERSION}/setup.sh -c && \
    chown -R user:user /home/user/.cmake \
    '

WORKDIR /zephyr-workspace/fprime-zephyr-app
ENTRYPOINT ["/bin/bash"]
