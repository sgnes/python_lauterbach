# python_lauterbach

A python implementation to control Lauterbach Trace32 software.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
lauterbach-trace32-rcl 
```

### Installing


```
pip install lauterbach-trace32-rcl 

```

## What this tool can do

This tool will open a trace32 software, and provide below functionlity:

1. Download elf file;
2. Run cmm script;
3. Read/Write global variable;

## Why this tool

You should already know that Canalyzer support CAPL script, so why create this new tool?

This tool is part of [EcuAutoTest](https://github.com/sgnes/EcuAutoTest),  EcuAutoTest is used to control Vector CANalyzer and CANape in one script, to do some ECU auto test.

### A demo:

```python
from python_lauterbach import python_lauterbach

with PythonLauterbach("C:/Lauterbach/T32_2022-02", "D:/test/debug.elf", "D:/test/setup.cmm") as debugger:
    # To read out a char TestArray[32] value;
    value = debugger.read_string_array_variable_value("TestArray", 32)
    # To read out a char *TestPointerArray[32] value;
    value = debugger.read_string_pointer_variable_value("TestPointerArray", 32)
    # To write a global arrary variable char TestArray[32] with data "AABBCC"
    debugger.write_string_array_variable_value("TestArray", "AABBCC")
    # To raed a none variable value, TestArray[1]
    value = debugger.read_variable_value("TestArray[1]")
    # To write a none variable value, TestArray[1]
    debugger.write_variable_value("TestArray[1]", "A")

```


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/sgnes/PythonCanalyzer/tags). 

## Authors

* **[Sgnes](sgnes0514@gmail.com)** - *Initial work* - 

See also the list of [contributors](https://github.com/sgnes/python_lauterbach/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


