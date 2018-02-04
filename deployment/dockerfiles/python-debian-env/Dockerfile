#
# Python environment of my website
#

FROM python:3.6-slim-stretch

MAINTAINER gn01842919@gmail.com

# Change Shell
SHELL ["/bin/bash", "-c"]
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Setup project's name
ARG PROJECT_NAME=my_focus_news
ENV PROJECT_NAME ${PROJECT_NAME}

# Install Git and Vim
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests git vim -y && rm -rf /var/cache/apt && rm -rf /var/lib/apt/lists/*

# Set up Virtualenv
RUN pip install virtualenv && virtualenv --python=python3 /venv/"${PROJECT_NAME}"

# Install pip requirements
COPY requirements.txt /
RUN /venv/"${PROJECT_NAME}"/bin/pip install -r /requirements.txt && rm -f /requirements.txt

# Source code will be put under /source
VOLUME ["/source"]
WORKDIR /source

# Setup entry point
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Other settings
RUN echo "alias ll='ls -altr'" >> ~/.bashrc
CMD ["/bin/bash"]

# Use the following command to build and run:
#       docker build -t proj-env:001 . && docker run -ti --name pyenv --rm proj-env:001

