#!/bin/bash

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
swig -python -c++ flatten.i

g++ -std=c++17 -fPIC -O2 -W -pedantic -Wextra -I /usr/local/share/nlohmann -I /usr/local/share/simdjson $(pkg-config --cflags --libs python3) -c flatten.cc flatten_wrap.cxx

g++ -std=c++17 -fPIC -O2 -shared /usr/local/share/simdjson/simdjson.o flatten.o flatten_wrap.o -o _flatten.so

rm flatten.o flatten_wrap.o flatten_wrap.cxx
