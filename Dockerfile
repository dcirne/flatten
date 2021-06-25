# Copyright 2021 Dalmo Cirne
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM python:3.7-buster

# Set bash as shell
SHELL ["/bin/bash", "-c"]

# Create the deployment and other directories
RUN mkdir -p /workspace && \
    mkdir -p /usr/local/git && \
    mkdir -p /usr/local/share/nlohmann && \
    mkdir -p /usr/local/share/simdjson

# Working directory
WORKDIR /workspace

# Update system and install required dependencies
RUN apt-get update && \
    apt-get -y upgrade

# Install packages and tools
RUN set -eux && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        swig && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -U pytest

RUN set -eux && \
    cd /usr/local/git && \
    git clone https://github.com/nlohmann/json.git && \
    cp -r json/single_include/nlohmann/* /usr/local/share/nlohmann/

RUN set -eux && \
    cd /usr/local/git && \
    git clone https://github.com/simdjson/simdjson.git -b v0.7.1 && \
    cp simdjson/singleheader/simdjson.* /usr/local/share/simdjson/ && \
    cd /usr/local/share/simdjson && \
    g++ -std=c++17 -fPIC -O2 -c simdjson.cpp -o simdjson.o
