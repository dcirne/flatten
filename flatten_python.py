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
import json
from typing import Dict
from typing import List
from typing import Tuple


NAME_KEY = "name"
DEFAULT_KEY = "default"


def _validate_flatten_dictionary(flatten_dict: Dict, validation_list: List) -> Tuple[Dict, bool]:
    """ Private function to verify if all required keys are present in the flatten JSON

    Args:
        flatten_dict: A flatten JSON dictionary
        validation_list: A list with the validation rules

    Returns:
        A tuple containing the validated flatten dictionary and a flag indicating whether it is valid
    """
    for obj in validation_list:
        if NAME_KEY not in obj:
            continue

        required_key = obj[NAME_KEY]
        if required_key in flatten_dict:
            continue

        if DEFAULT_KEY not in obj:
            return (None, False)

        default_value = obj[DEFAULT_KEY]
        flatten_dict[required_key] = default_value

    return (flatten_dict, True)


def _flatten_dictionary(source_dict: Dict, target_dict: Dict, key: str, flatten_arrays: bool) -> Dict:
    """Private function to flatten a dictionary representing a JSON

    Args:
        source_dict: A Python dictionary containing a JSON representation
        target_dict: The target dictionary to contain the flatten JSON
        key: If a recursive call, the key of the parent object
        flatten_arrays: A flag indicating whether arrays should be flattened as well. Only the first element of the array would be picked

    Returns:
        A dictionary with the representation of the flatten JSON
    """
    for k, v in source_dict.items():
        dict_key = k if len(key.strip()) == 0 else key + "." + k

        if isinstance(v, dict):
            for nested_k, nested_v in _flatten_dictionary(v, target_dict, dict_key, flatten_arrays).items():
                target_dict[nested_k] = nested_v
        else:
            value_is_list = isinstance(v, List)

            if dict_key in target_dict:
                if flatten_arrays:
                    target_dict[dict_key] = v[0] if value_is_list else v
                else:
                    if value_is_list:
                        target_dict[dict_key].extend(v)
                    else:
                        target_dict[dict_key].append(v)
            else:
                if flatten_arrays:
                    target_dict[dict_key] = v[0] if value_is_list else v
                else:
                    target_dict[dict_key] = v

    return target_dict

def flatten_json(json_string: str, flatten_arrays: bool, validation_json: str) -> str:
    """Public function to flatten a JSON string.
    It takes a JSON string and returns a flattened equivalent.

    Args:
        json_string: The JSON string to be flattened
        flatten_arrays: A flag indicating whether arrays should be flattened as well. Only the first element of the array would be picked
        validation_json: A JSON string with the name of the keys expected to be present in the flatten JSON, the data type, and the default value in case the key is not present

    Returns:
        A flatten JSON string
    """
    json_dict = json.loads(json_string)
    flatten_dict = {}
    flatten_dict = _flatten_dictionary(json_dict, flatten_dict, "", flatten_arrays)

    if len(validation_json) > 0:
        validation_list = json.loads(validation_json)
        (flatten_dict, valid) = _validate_flatten_dictionary(flatten_dict, validation_list)

        if valid:
            return json.dumps(flatten_dict)
        else:
            return ""
    else:
        return json.dumps(flatten_dict)
