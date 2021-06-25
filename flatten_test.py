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
import pytest


def test_flatten_python():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    with open('validation.json', 'r') as validation_file:
        validation_json = validation_file.read()

    flatten_arrays = False
    flatten_str = flatten_python.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)

    flatten_dict = json.loads(flatten_str)
    assert(len(flatten_dict) == 10)
    assert(flatten_dict["isbn"] == "123-456-222")
    assert(flatten_dict["author.lastname"] == "Doe")
    assert(flatten_dict["author.firstname"] == "Jane")
    assert(flatten_dict["editor.lastname"] == "Smith")
    assert(flatten_dict["editor.firstname"] == "Jane")
    assert(flatten_dict["title"] == "The Ultimate Book in the Universe")
    assert(flatten_dict["category"] == ["Non-Fiction", "Technology"])
    assert(flatten_dict["price"] == 3.14)
    assert(flatten_dict["Number of pages"] == 42)
    assert(flatten_dict["genre"] == "Unknown")

def test_flatten_cpp():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    with open('validation.json', 'r') as validation_file:
        validation_json = validation_file.read()

    flatten_arrays = False
    flatten_str = flatten.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)

    flatten_dict = json.loads(flatten_str)
    assert(len(flatten_dict) == 10)
    assert(flatten_dict["isbn"] == "123-456-222")
    assert(flatten_dict["author.lastname"] == "Doe")
    assert(flatten_dict["author.firstname"] == "Jane")
    assert(flatten_dict["editor.lastname"] == "Smith")
    assert(flatten_dict["editor.firstname"] == "Jane")
    assert(flatten_dict["title"] == "The Ultimate Book in the Universe")
    assert(flatten_dict["category"] == ["Non-Fiction", "Technology"])
    assert(flatten_dict["price"] == 3.14)
    assert(flatten_dict["Number of pages"] == 42)
    assert(flatten_dict["genre"] == "Unknown")

def test_flatten_python_including_arrays():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    with open('validation.json', 'r') as validation_file:
        validation_json = validation_file.read()

    flatten_arrays = True
    flatten_str = flatten_python.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)

    flatten_dict = json.loads(flatten_str)
    assert(len(flatten_dict) == 10)
    assert(flatten_dict["isbn"] == "123-456-222")
    assert(flatten_dict["author.lastname"] == "Doe")
    assert(flatten_dict["author.firstname"] == "Jane")
    assert(flatten_dict["editor.lastname"] == "Smith")
    assert(flatten_dict["editor.firstname"] == "Jane")
    assert(flatten_dict["title"] == "The Ultimate Book in the Universe")
    assert(flatten_dict["category"] == "Non-Fiction")
    assert(flatten_dict["price"] == 3.14)
    assert(flatten_dict["Number of pages"] == 42)
    assert(flatten_dict["genre"] == "Unknown")

def test_flatten_cpp_including_arrays():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    with open('validation.json', 'r') as validation_file:
        validation_json = validation_file.read()

    flatten_arrays = True
    flatten_str = flatten.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)

    flatten_dict = json.loads(flatten_str)
    assert(len(flatten_dict) == 10)
    assert(flatten_dict["isbn"] == "123-456-222")
    assert(flatten_dict["author.lastname"] == "Doe")
    assert(flatten_dict["author.firstname"] == "Jane")
    assert(flatten_dict["editor.lastname"] == "Smith")
    assert(flatten_dict["editor.firstname"] == "Jane")
    assert(flatten_dict["title"] == "The Ultimate Book in the Universe")
    assert(flatten_dict["category"] == "Non-Fiction")
    assert(flatten_dict["price"] == 3.14)
    assert(flatten_dict["Number of pages"] == 42)
    assert(flatten_dict["genre"] == "Unknown")

def test_invalid_json_python():
    json_data = '{"invalid":'
    with pytest.raises(Exception):
        flatten_str = flatten_python.flatten_json(json_data, False, "")
        assert(len(flatten_str) == 0)
        assert(flatten_str == "")

def test_invalid_json_cpp():
    json_data = '{"invalid":'
    flatten_str = flatten.flatten_json(json_data, False, "")
    assert(len(flatten_str) == 0)
    assert(flatten_str == "")

def test_empty_json_python():
    json_data = ""
    with pytest.raises(Exception):
        flatten_str = flatten_python.flatten_json(json_data, False, "")
        assert(len(flatten_str) == 0)
        assert(flatten_str == "")

def test_empty_json_cpp():
    json_data = ""
    flatten_str = flatten.flatten_json(json_data, False, "")
    assert(len(flatten_str) == 0)
    assert(flatten_str == "")

def test_invalid_validation_python():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    validation_json = '[{"name":"missing_field_with_no_default"}]'

    flatten_arrays = True
    flatten_str = flatten_python.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)
    assert(flatten_str == "")

def test_invalid_validation_cpp():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    validation_json = '[{"name":"missing_field_with_no_default"}]'

    flatten_arrays = True
    flatten_str = flatten.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)
    assert(flatten_str == "")

def test_empty_validation_python():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    validation_json = ""

    flatten_arrays = False
    flatten_str = flatten_python.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)

    flatten_dict = json.loads(flatten_str)
    assert(len(flatten_dict) == 9)
    assert(flatten_dict["isbn"] == "123-456-222")
    assert(flatten_dict["author.lastname"] == "Doe")
    assert(flatten_dict["author.firstname"] == "Jane")
    assert(flatten_dict["editor.lastname"] == "Smith")
    assert(flatten_dict["editor.firstname"] == "Jane")
    assert(flatten_dict["title"] == "The Ultimate Book in the Universe")
    assert(flatten_dict["category"] == ["Non-Fiction", "Technology"])
    assert(flatten_dict["price"] == 3.14)
    assert(flatten_dict["Number of pages"] == 42)

def test_empty_validation_cpp():
    with open('sample.json', 'r') as json_file:
        json_data = json_file.read()

    validation_json = ""

    flatten_arrays = False
    flatten_str = flatten.flatten_json(json_data, flatten_arrays, validation_json)
    assert(flatten_str is not None)

    flatten_dict = json.loads(flatten_str)
    assert(len(flatten_dict) == 9)
    assert(flatten_dict["isbn"] == "123-456-222")
    assert(flatten_dict["author.lastname"] == "Doe")
    assert(flatten_dict["author.firstname"] == "Jane")
    assert(flatten_dict["editor.lastname"] == "Smith")
    assert(flatten_dict["editor.firstname"] == "Jane")
    assert(flatten_dict["title"] == "The Ultimate Book in the Universe")
    assert(flatten_dict["category"] == ["Non-Fiction", "Technology"])
    assert(flatten_dict["price"] == 3.14)
    assert(flatten_dict["Number of pages"] == 42)
