# Flatten module

Here you will find a C++ implementation of a JSON flattener that you can use in Python. In the sample test it performs about 4 times faster than its pure Python equivalent implementation. Your actual mileage may vary.

We use [SWIG](http://swig.org) to generate the wrapper to expose the C++ function to be used in native Python. 


## Building

The module is built (compiled, linked, and generation of the Python wrapper) inside of a Docker container. You shoud be able to copy the generated files (`_flatten.so` and `flatten.py`) and use in your code without any problems. 

**Build the Docker image**

```bash
docker build -f Dockerfile -t flatten --rm .
```

**Run the Docker image**

The Docker container will use your local directory with this project and mount it in a shared volume inside of the container. The working directory is: `workspace`.

```bash
docker run --rm -it -v $(pwd):/workspace flatten /bin/bash
```


## Generating the module

Once in the Docker container, just run the build script. If you look inside you will see that it generated a Python wrapper using SWIG with the configuration informed in the inteface file: `flatten.i`

```bash
./build.sh
```

A few files will be generated, but the only files of interest to include in your project are:

* `_flatten.so`
* `flatten.py`


## Usage

Copy `_flatten.so` and `flatten.py` to the directory of your code and import the Python module.

For example:

```python
import flatten
```

or

```python
from flatten import flatten_json
```

Then call the `flatten_json` function passing as parameters a JSON string (binary), a flag indicating whether to also flatten lists, and a validation JSON to verify that required keys are present and/or have default values. The function returns a flatten JSON string.

The function signature is:

```python
def flatten_json(json_string: str, flatten_arrays: bool, validation_json: str) -> str:
```

### The validation JSON

In case you want to validate the flattened JSON for required keys and/or default values if a value is missing, the schema of the validation JSON is as follows:

```js
[
    {
        "name": "Required field name",
        "type": "Data type",
        "default": "Default value [str, int, float, bool]"
    }
]
```

You can see an example in the [`validation.json`](validation.json) file.


## Running the main program

In order to measure the persormance, you will find a `flatten_python.py` file that implements the flattening of a JSON purely in Python.

There is also a `main.py` file, that uses both modules. The one implemented in Python and the one implemented in C++. The sample code measures the time it takes to flatten a simple JSON and prints out the results.

Run it with:

```bash
python main.py
```


## Testing

Testing the expected behavior is simple and can be done after generating the module. Once the module is generate just run:

```bash
pytest flatten_test.py
```


## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). See the LICENSE file for more info.
