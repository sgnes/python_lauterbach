# python_lauterbach

A python implementation to control Lauterbach Trace32 software.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
lauterbach-trace32-rcl 
```

Add below two line in your T32 config file(C:\T32\config.t32 normally)

```
RCL=NETTCP
PORT=20000
```

### Installing


```
pip install lauterbach-trace32-rcl 

```

## What this tool can do

This tool will open a trace32 software, and provide below functionlity:

1. Download elf/hex file;
2. Run cmm script;
3. Read/Write global variable;

## Why this tool



This tool is part of [EcuAutoTest](https://github.com/sgnes/EcuAutoTest),  EcuAutoTest is used to control ECU software for testing, to do some ECU auto test.

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

### Parameters

            t32_path (string): T32 full path, "C:\T32\bin\windows64\t32mtc.exe" for Aurix.
            elf_path (string): full path of the elf file for debug.
            setup_cmm (string): a setup a cmm file, setup cpu, mutil core setting...
            cpu (str, optional): CPU model. Defaults to "TC387QP".
            flash_cmm (str, optional): the flash cmm privded by Lauterbach. Defaults to "~~/demo/tricore/flash/tc38x.cmm".
            hex_file (string, optional): hex file name. Defaults to None.
            logger (object, optional): logger object. Defaults to None.
            t32_config (str, optional): T32 connfig file. Defaults to "config.t32".
            protocol (str, optional): RCL protocol. Defaults to "TCP".
            node (str, optional): RCL host. Defaults to "localhost".
            port (int, optional): RCL Port. Defaults to 20000.


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/sgnes/PythonCanalyzer/tags). 

## Authors

* **[Sgnes](sgnes0514@gmail.com)** - *Initial work* - 

See also the list of [contributors](https://github.com/sgnes/python_lauterbach/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


