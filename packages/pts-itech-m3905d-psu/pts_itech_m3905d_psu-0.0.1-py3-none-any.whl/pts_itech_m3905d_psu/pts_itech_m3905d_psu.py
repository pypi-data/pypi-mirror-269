import logging
import time
import pyvisa
from typing import Union, Tuple, Literal


class ITechM3905DPSU:
    """
    ``Base class for the ITech M3905D PSU``
    """
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.getLogger().setLevel(logging.INFO))

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.resource_manager = None
        self.itech_psu = None

    def open_connection(self):
        """
        Opens a TCP/IP connection to the ITech M3905D PSU \n
        """
        self.resource_manager = pyvisa.ResourceManager()
        try:
            logging.debug(f": Opening PSU Resource at {self.connection_string}")
            self.itech_psu = self.resource_manager.open_resource(self.connection_string)
            self.itech_psu.read_termination = '\n'
            self.itech_psu.write_termination = '\n'
        except Exception as e:
            raise Exception(f": ERROR {e}: Could not open Resource\n")

    def close_connection(self):
        """
        Closes the TCP/IP connection to the ITech M3905D PSU \n
        """
        self.resource_manager.close()

    def identity(self) -> str:
        """
        This command is used to query the IDN of the device. \n
        """
        idn = self.itech_psu.query(f'*IDN?')
        return str(idn)

    def scpi_version(self) -> str:
        """
        This command is used to query the version number of the used SCPI command. \n
        """
        scpi_version = self.itech_psu.query(f'SYSTem:VERSion?')
        return str(scpi_version)

    def reset(self) -> None:
        """
        Resets the instrument to pre-defined values that are either typical or safe. \n
        """
        self.itech_psu.write(f'*RST')

    def system_remote(self) -> None:
        """
        This command is used to set the instrument to the remote control mode via the communication interface. \n
        """
        self.itech_psu.write(f'SYST:REM')

    def system_local(self) -> None:
        """
        This command is used to set the instrument to local mode, i.e. panel control mode. \n
        """
        self.itech_psu.write(f'SYST:LOC')

    def system_error(self) -> str:
        """
        This command is used to query the error information of the instrument. \n
        """
        sys_err = self.itech_psu.query(f'SYST:ERR?')
        return str(sys_err)

    def system_clear_error_queue(self) -> None:
        """
        This command is used to clear the error queue. \n
        """
        self.itech_psu.write(f'SYST:CLE')

    def get_ip_address(self) -> str:
        """
        This command is used to query the IP address of the instrument. \n
        """
        ip_address = self.itech_psu.query(f"SYST:COMM:LAN:IP?")
        return str(ip_address)

    def get_subnetmask(self) -> str:
        """
        This command is used to query the subnet mask of the LAN communication. \n
        """
        subnet_mask = self.itech_psu.query(f"SYST:COMM:LAN:SMAS?")
        return str(subnet_mask)

    def selftest(self) -> bool:
        """
        Self-test query. Performs an instrument self-test. If self-test fails, one or more error messages will provide additional information. \n
        :return: True or False \n
        """
        try:
            test = self.itech_psu.query(f'*TST?')
            if test == '0':
                logging.debug(f"PASS")
                return True
            else:
                logging.error(f"ERROR: {self.system_error()}")
                return False
        except Exception as e:
            raise Exception(f"ERROR: Cannot run Selftest: {e}")

    def set_mode(self, mode: Literal['VOLT', 'CURR']) -> None:
        """
        This command is used to set the working mode of the power supply. \n
        VOLTage: Indicates that the power supply is operating in CV priority mode \n
        CURRent: Indicates that the power supply is operating in CC priority mode \n
        :param mode: 'VOLT' or 'CURR' \n
        """
        self.itech_psu.write(f"FUNCtion {str(mode)}")

    def get_mode(self) -> str:
        """
        This command is used to query the working mode of the power supply.\n
        :return: 'VOLTage' or 'CURRent' \n
        """
        mode = self.itech_psu.query(f"FUNCtion?")
        return str(mode)

    def set_voltage(self, voltage: Union[float, str]) -> None:
        """
        This command is used to set the output voltage value Vset in CV priority mode \n
        :param voltage: MINimum|MAXimum|DEFault|<value> ; Setting range: MIN to MAX; value: 0-10V \n
        """
        self.itech_psu.write(f"VOLT {voltage}")

    def get_voltage(self) -> str:
        """
        This command is used to query the output voltage value Vset in CV priority mode. \n
        """
        voltage = self.itech_psu.query(f"VOLT?")
        return str(voltage)

    def set_current(self, current: Union[float, str]) -> None:
        """
        This command is used to set the output current value Iset in CC priority mode \n
        :param current:MINimum|MAXimum|DEFault|<value> ; Setting range: MIN to MAX; value: 0-510A \n
        """
        self.itech_psu.write(f"CURRent {current}")

    def get_current(self) -> str:
        """
        This command is used to query the output current value Iset in CC priority mode \n
        """
        current = self.itech_psu.query(f"CURR?")
        return str(current)

    def output_on(self) -> None:
        """
        Enable the output. \n
        """
        self.itech_psu.write(f"OUTP 1")

    def output_off(self) -> None:
        """
        Disable the output. \n
        """
        self.itech_psu.write(f"OUTP 0")

    def output_status(self) -> str:
        """
        This command is used to query the status of the output: enabled or disabled. \n
        """
        status = self.itech_psu.query(f"OUTP?")
        return str(status)

    def set_voltage_upper_limit(self, voltage_ul: Union[float, str]) -> None:
        """
        This command is used to set the voltage upper limit value Vlim in CC priority mode \n
        :param voltage_ul: MINimum|MAXimum|DEFault|<value>; value: 0-10V; Setting range: MIN to MAX \n
        """
        try:
            self.itech_psu.write(f"VOLT:LIM {voltage_ul}")
            time.sleep(0.5)
            err = self.system_error()
            if err == '0,"No error"':
                logging.debug(f": Voltage Upper Limit set to {voltage_ul}")
            else:
                raise SystemError(f"ERROR {err} while executing command.")
        except Exception as e:
            raise Exception(f"ERR: {e}: Cannot set voltage upper limit")

    def set_voltage_lower_limit(self, voltage_ll: Union[float, str]) -> None:
        """
        This command is used to set the voltage lower limit value Vl in CC priority mode \n
        :param voltage_ll: MINimum|MAXimum|DEFault|<value>; value: 0-10V; Setting range: MIN to MAX \n
        """
        try:
            self.itech_psu.write(f"VOLT:LIM:NEG {voltage_ll}")
            time.sleep(0.5)
            err = self.system_error()
            if err == '0,"No error"':
                logging.debug(f": Voltage Lower Limit set to {voltage_ll}")
            else:
                raise SystemError(f"ERROR {err} while executing command.")
        except Exception as e:
            raise Exception(f"ERR: {e}: Cannot set voltage lower limit")

    def get_voltage_limits(self) -> Tuple:
        """
        This command is used to query the voltage upper limit value Vlim and voltage lower limit value Vl in CC priority mode. \n
        """
        volt_ul = self.itech_psu.query(f"VOLT:LIM?")
        time.sleep(0.5)
        volt_ll = self.itech_psu.query(f"VOLT:LIM:NEG?")
        time.sleep(0.5)
        err = self.system_error()
        if err == '0,"No error"':
            if volt_ul and volt_ll:
                return str(volt_ll), str(volt_ul)
            else:
                logging.error(f"Volt ul : {volt_ul} and Volt ll: {volt_ll}")
                raise ValueError(f'ERR: One of the values is None')
        else:
            raise ValueError(f"ERR: {err} Cannot get voltage limits")

    def set_current_upper_limit(self, curr_ul: Union[float, str]) -> None:
        """
        This command is used to set the current upper limit value Ilim value in CV priority mode \n
        :param curr_ul: MINimum|MAXimum|DEFault|<value>; value: 0-510A; Setting range: MIN to MAX \n
        """
        try:
            self.itech_psu.write(f"CURR:LIM {curr_ul}")
            time.sleep(0.5)
            err = self.system_error()
            if err == '0,"No error"':
                logging.debug(f": Current Upper Limit set to {curr_ul}")
            else:
                raise SystemError(f"ERROR {err} while executing command.")
        except Exception as e:
            raise Exception(f"ERR: {e}: Cannot set current limit")

    def set_current_lower_limit(self, curr_ll: Union[float, str]) -> None:
        """
        This command is used to set the current lower limit value I- in CV priority mode \n
        :param curr_ll: MINimum|MAXimum|DEFault|<value> ; value: 0-510A; Setting range: MIN to MAX \n
        """
        try:
            self.itech_psu.write(f"CURR:LIM:NEG {curr_ll}")
            time.sleep(0.5)
            err = self.system_error()
            if err == '0,"No error"':
                logging.debug(f": Current Lower Limit set to {curr_ll}")
            else:
                raise SystemError(f"ERROR {err} while executing command.")
        except Exception as e:
            raise Exception(f"ERR: {e}: Cannot set current limit")


    def get_current_limits(self) -> Tuple:
        """
        This command is used to query the current upper limit value Ilim and current lower limit value I- in CV priority mode. \n
        """
        curr_ul = self.itech_psu.query(f"CURR:LIM?")
        time.sleep(0.5)
        curr_ll = self.itech_psu.query(f"CURR:LIM:NEG?")
        time.sleep(0.5)
        err = self.system_error()
        if err == '0,"No error"':
            if curr_ul and curr_ll:
                return str(curr_ul), str(curr_ll)
            else:
                logging.error(f"Current ul : {curr_ul} and Current ll: {curr_ll}")
                raise ValueError(f'ERR: One of the values is None')
        else:
            raise ValueError(f"ERR: {err} Cannot get current limits")
