// Copyright 2021 Dalmo Cirne
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#include <functional>
#include <string>
#include "json.hpp"
#include "simdjson.h"


const std::string name_key("name");
const std::string type_key("type");
const std::string default_key("default");

/** @brief Verify if all required keys are present in the flatten JSON
 * @details Iterates over the required_keys vector and verify that all of them are present in the flatten JSON
 *
 * @param[in,out] json_obj A flatten JSON object
 * @param[in] validation_obj A parsed simdjson containing the validation parameters the flatten JSON object
 * @return True if JSON can be validated, false otherwise
 */
bool validate_flatten_json(nlohmann::json &json_obj, const simdjson::dom::array &validation_array) {
    for (const auto &obj : validation_array) {
        const auto [required_key, error_code] = obj[name_key];

        if (error_code != simdjson::error_code::SUCCESS) {
            continue;
        }

        const auto required_key_str = std::string(required_key);

        if (!json_obj.contains(required_key_str)) {
            const auto default_value = obj[default_key];
            
            if (default_value.error() == simdjson::error_code::NO_SUCH_FIELD) {
                return false;
            } else {
                switch (default_value.type()) {
                    case simdjson::dom::element_type::STRING:
                        json_obj[required_key_str] = std::string(default_value);
                        break;
                    case simdjson::dom::element_type::INT64:
                        json_obj[required_key_str] = int64_t(default_value);
                        break;
                    case simdjson::dom::element_type::UINT64:
                        json_obj[required_key_str] = uint64_t(default_value);
                        break;
                    case simdjson::dom::element_type::DOUBLE:
                        json_obj[required_key_str] = double(default_value);
                        break;
                    case simdjson::dom::element_type::BOOL:
                        json_obj[required_key_str] = bool(default_value);
                        break;
                    default:
                        break;
                }
            }
        }
    }

    return true;
}

/** @brief Flattens a JSON
 * @details This function uses two JSON libraries. simdjson, which is a super fast parser
 * and nlohmann, which is a super fast generator
 *
 * @param[in] source_obj A parsed simdjson object (dictionary)
 * @param[in,out] target_obj The target object that will contain the flatten JSON
 * @param[in] target_key If a recursice call, the key of the parent object
 * @param[in] flatten_arrays A flag indicating whether arrays should be flattened as well. Only the first element of the array would be picked
 * @return void
 */
void flatten_json(const simdjson::dom::object &source_obj, nlohmann::json &target_obj, const std::string &target_key, const bool flatten_arrays) {
    // Lambda function to transform a simdjson element into C++ data type and add it to a nlohmann array
    const auto add_element_to_array = [&target_obj](const simdjson::dom::element &element, const std::string &key) {
        switch (element.type()) {
            case simdjson::dom::element_type::INT64:
                target_obj[key].push_back(int64_t(element));
                break;
            case simdjson::dom::element_type::UINT64:
                target_obj[key].push_back(uint64_t(element));
                break;
            case simdjson::dom::element_type::DOUBLE:
                target_obj[key].push_back(double(element));
                break;
            case simdjson::dom::element_type::STRING:
                target_obj[key].push_back(std::string(element));
                break;
            case simdjson::dom::element_type::BOOL:
                target_obj[key].push_back(bool(element));
                break;
            default:
                break;
        }
    };

    // Lambda function to transform a simdjson array into a nlohmann array
    const auto add_array_elements = [&target_obj, &add_element_to_array](const simdjson::dom::element &array, const std::string &key) {
        for (const auto &element : array) {
            add_element_to_array(element, key);
        }
    };

    // Lambda function to transform a simdjson element into a equivalent nlohmann
    const std::function<void(const simdjson::dom::element &, const std::string &)> add_element = [&](const simdjson::dom::element &element, const std::string &key) {
        switch (element.type()) {
            case simdjson::dom::element_type::STRING:
                target_obj[key] = std::string(element);
                break;
            case simdjson::dom::element_type::INT64:
                target_obj[key] = int64_t(element);
                break;
            case simdjson::dom::element_type::UINT64:
                target_obj[key] = uint64_t(element);
                break;
            case simdjson::dom::element_type::DOUBLE:
                target_obj[key] = double(element);
                break;
            case simdjson::dom::element_type::ARRAY:
                if (flatten_arrays) {
                    for (const auto &array_element : element.get_array()) {
                        add_element(array_element, key);
                        break;
                    }
                } else {
                    add_array_elements(element, key);
                }
                break;
            case simdjson::dom::element_type::BOOL:
                target_obj[key] = bool(element);
                break;
            default:
                break;
        }
    };

    // Loop to flatten the JSON (with recursive calls)
    for (const auto &[key, value] : source_obj) {
        const std::string key_string(key);
        const std::string flatten_key = !target_key.empty() ? target_key + "." + key_string : key_string;

        if (value.is_object()) {
            flatten_json(value, target_obj, flatten_key, flatten_arrays);
        } else {
            if (target_obj.contains(flatten_key)) {
                if (value.is_array()) {
                    add_array_elements(value, flatten_key);
                } else {
                    const auto previous_value = target_obj[flatten_key];
                    target_obj.erase(flatten_key);
                    target_obj[flatten_key].push_back(previous_value);
                    add_element_to_array(value, flatten_key);
                }
            } else {
                add_element(value, flatten_key);
            }
        }
    }
}

/** @brief Public function to flatten a JSON string
 * @details This function takes a JSON string and returns a flattened equivalent
 *
 * @param[in] json_string The JSON string to be flattened
 * @param[in] flatten_arrays A flag indicating whether arrays should be flattened as well. Only the first element of the array would be picked
 * @param[in] validation_json A JSON string with the name of the keys expected to be present in the flatten JSON, the data type, and the default value in case the key is not present
 * @return A flatten JSON string
 */
std::string flatten_json(const std::string &json_string, const bool flatten_arrays, const std::string &validation_json) {
    simdjson::dom::parser json_parser;
    simdjson::padded_string json_padded_string(json_string);
    simdjson::dom::object root_obj;
    auto error = json_parser.parse(json_padded_string).get(root_obj);

    if (error) {
        return "";
    }

    nlohmann::json target_obj;
	std::string target_key;

    flatten_json(root_obj, target_obj, target_key, flatten_arrays);

    if (target_obj.is_object()) {
        if (validation_json.empty()) {
            return target_obj.dump();
        } else {
            json_padded_string = simdjson::padded_string(validation_json);
            simdjson::dom::array validation_array;
            error = json_parser.parse(json_padded_string).get(validation_array);

            if (error) {
                return "";
            }

            const bool valid = validate_flatten_json(target_obj, validation_array);
            if (valid) {
                return target_obj.dump();
            } else {
                return "";
            }
        }
    } else {
        return "";
    }
}
