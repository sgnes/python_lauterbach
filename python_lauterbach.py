"""Basic functions related to software testing with Lauterbach"""
import subprocess
import os
import time
import logging
from logging import config
import lauterbach.trace32.rcl as t32

log_config = {
    "version":1,
    "root":{
        "handlers" : ["console"],
        "level": "DEBUG"
    },
    "handlers":{
        "console":{
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        }
    },
    "formatters":{
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s)) Log : %(message)s",
            "datefmt":"%d-%m-%Y %I:%M:%S"
        }
    },
}


class PythonLauterbach():
    """A python lib to easy connect with Lauterbach"""
    def __init__(self,t32_path, elf_path, setup_cmm, logger=None, t32_config="config.t32", protocol="TCP", node="localhost", port=20000) -> None:
        if not logger:
            config.dictConfig(log_config)
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Enter init with parameters %s  %s, %s", t32_path, elf_path, setup_cmm)
        self._t32_path = t32_path
        if os.path.exists(self._t32_path):
            self._t32_root = self._t32_path.split("bin")[0]
        else:
            raise FileNotFoundError(f"T32 exe file not found, please check the input: {t32_path}.")
        if not os.path.exists(setup_cmm):
            self._setup_cmm = os.path.join(self._t32_root, setup_cmm)
            if not os.path.exists(self._setup_cmm):
                raise FileNotFoundError(f"T32 setup cmm file not found, please check the input: {self._setup_cmm}.")
        else:
            self._setup_cmm = setup_cmm
        if not os.path.exists(t32_config):
            self._t32_config = os.path.join(self._t32_root, t32_config)
            if not os.path.exists(self._t32_config):
                raise FileNotFoundError(f"T32 setup cmm file not found, please check the input: {self._t32_config}.")
        self.elf_file = os.path.realpath(elf_path)
        self.node = node
        self.protocol = protocol
        self.port = port
        self._debugger_process = None
        self.dbg = None

    def __enter__(self):
        self.logger.info("Enter __enter__")
        self._debugger_process = subprocess.Popen([self._t32_path, '-c', self._t32_config])
        time.sleep(5)
        self.dbg = t32.connect(node=self.node, port=self.port, protocol=self.protocol, timeout=10.0)
        self.dbg.cmd('Area.Reset')
        self.dbg.cmm(self._setup_cmm)
        self.dbg.cmd(r"system.up")
        if os.path.exists(self.elf_file):
            self.dbg.cmd(f'Data.LOAD.Elf "{self.elf_file}" /DIFF /SingleLineAdjacent')
            #TODO: to be removed if use the system.detect cpu to detect the right cpu
            self.dbg.cmd("DO ~~/demo/tricore/flash/tc38x.cmm CPU=TC387QP PREPAREONLY")
            time.sleep(10)
            self.dbg.cmd("FLASH.ReProgram ALL")
            time.sleep(3)
            self.dbg.cmd(f'Data.LOAD.Elf {os.path.realpath(self.elf_file)}')
            time.sleep(3)
            self.dbg.cmd("FLASH.ReProgram OFF")
            time.sleep(10)
        self.dbg.cmd(r"system.up")
        self.dbg.cmd(r"go")
        self.logger.info("Exit __enter__")
        return self
        

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Enter __exit__")
        if self.dbg:
            self.dbg.cmd("QUIT")
            self.dbg = None
        
        self.logger.info("Exit __exit__")
        pass

    def __del__(self):
        self.logger.info("Enter __del__")
        if self.dbg:
            self.dbg.cmd("QUIT")
            self.dbg = None

    def load_symbol_from_elf(self, elf):
        """load symbol from a elf file, this will not download dat to MCU.

        Args:
            elf (str): elf file name
        """
        if os.path.exists(elf):
            self.dbg.cmd(f'Data.LOAD.Elf "{elf}" /nocode')
        else:
            raise FileNotFoundError(f"Elf file not exist:{elf}")

    def read_string_array_variable_value(self, var, max_len):
        """Get the value of a string arrary global variable, return a string.
        char global_test_var[15];
        var should use global_test_var, max_len should be 15.

        Args:
            var (string): global string array variable name, whitout"[]"
            max_len (int): maximum length of the string, if found 0, it will returns

        Returns:
            _type_: the sting
        """
        tmp_list = []
        for i in range(0,max_len,1):
            tmp = self.dbg.variable.read(f"{var}[{i}]").value
            if tmp > 0:
                tmp_list.append(chr(tmp))
            else:
                break
        return "".join(tmp_list)

    def read_string_pointer_variable_value(self, var, max_len):
        """Get the value of a string arrary global variable, return a string.
        char global_test_var[15];
        var should use global_test_var, max_len should be 15.

        Args:
            var (string): global string array variable name, whitout"[]"
            max_len (int): maximum length of the string, if found 0, it will returns

        Returns:
            _type_: the sting
        """
        tmp_list = []
        tmp_addr = self.dbg.memory.read_uint32(address=self.dbg.address(access='D', value=self.dbg.symbol.query_by_name(name=var).address.value))
        for i in range(0,max_len,1):
            tmp = self.dbg.memory.read_uint8(address=self.dbg.address(access='D', value=tmp_addr))
            tmp_addr += 1
            if tmp > 0:
                tmp_list.append(chr(tmp))
            else:
                break
        return "".join(tmp_list)

    def write_string_array_variable_value(self, var, value):
        """Write the value of a string arrary global variable, return a string.

        Args:
            var (string): global string array variable name, whitout"[]"
            max_len (int): maximum length of the string, if found 0, it will returns

        Returns:
            _type_: 0 means write without issue.
        """
        for i in range(0,len(value),1):
            self.dbg.variable.write(f"{var}[{i}]", value[i])
            
        return 0

    def read_variable_value(self, var):
        """read variable value

        Args:
            var (str): var name

        Returns:
            _type_: var value
        """
        return self.dbg.variable.read(var).value
    
    def write_variable_value(self, var, value):
        """write variable value

        Args:
            var (str): var name
            value (str): var value

        Returns:
            _type_: var value
        """
        return self.dbg.variable.write(var, value)


