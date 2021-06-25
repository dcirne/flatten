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
import flatten # Python module containing the C++ implementation
import flatten_python # Pure Python implementation
import json
from time import time


if __name__ == "__main__":
    # Loads the sample JSON file
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    # Loads the validation JSON file
    with open('validation.json', 'r') as validation_file:
        validation_json = validation_file.read()

    number_iterations = 100000
    flatten_arrays = True

    # Measures how long a pure Python implementation takes to flatten a JSON
    start = time()
    for _ in range(number_iterations):
        flatten_str = flatten_python.flatten_json(json_data, flatten_arrays, validation_json)

    print("Python time: {0} seconds".format(time() - start))
    print(flatten_str)

    # Measures how long a hybrid Python/C++ implementation takes to flatten a JSON
    start = time()
    for _ in range(number_iterations):
        flatten_str = flatten.flatten_json(json_data, flatten_arrays, validation_json)

    print("\nC++ time: {0} seconds".format(time() - start))
    print(flatten_str)
