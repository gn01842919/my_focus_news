#
# Python environment for my projects
#

FROM python:3.6-slim-stretch

MAINTAINER gn01842919@gmail.com

# Change Shell
SHELL ["/bin/bash", "-c"]
RUN rm /bin/sh && ln -s /bin/bash /bin/sh


# Source code will be put here
VOLUME ["/src"]
WORKDIR /src


# Setup entry point to activate virtualenv at start up
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


# Other settings
RUN echo "alias ll='ls -altr'" >> ~/.bashrc
CMD ["/bin/bash"]


# Install Virtualenv
RUN pip install virtualenv


# Setup project's name
ARG PROJECT_NAME
ENV PROJECT_NAME ${PROJECT_NAME}

# Set up Virtualenv
RUN virtualenv --python=python3 /venv/${PROJECT_NAME}

# Install pip requirements
COPY "${PROJECT_NAME}-requirements.txt" /requirements.txt
RUN /venv/${PROJECT_NAME}/bin/pip install -r /requirements.txt && rm -f /requirements.txt
