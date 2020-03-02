FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Or your actual UID, GID on Linux if not the default 1000
ARG USERNAME=root
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# System
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    && apt-get install --yes locales \
    && rm -rf /var/lib/apt/lists/* /var/cache/debconf \
    && apt-get clean

# Files
COPY requirements.txt /tmp/pip-tmp/

# Update Python environment based on requirements.txt
RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp \
    # Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
    && groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd -s /bin/bash --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
    # [Optional] Add sudo support for the non-root user
    && sed -i 's/deb.debian.org/opensource.nchc.org.tw/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get -y install sudo \
    && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

# set default language environment
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"
ENV LANGUAGE="en_US.UTF-8"

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

COPY startScript.sh /startScript.sh
CMD ["/bin/sh", "/startScript.sh"]
