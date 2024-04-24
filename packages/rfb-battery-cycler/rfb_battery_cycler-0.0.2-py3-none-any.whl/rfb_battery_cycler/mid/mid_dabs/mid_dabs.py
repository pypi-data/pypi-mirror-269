#!/usr/bin/python3
#pylint: disable= fixme
"""
This module will create instances of epc device in order to control
the device and request info from it.
"""
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
from typing import List #, Dict
#######################         GENERIC IMPORTS          #######################

#######################       THIRD PARTY IMPORTS        #######################

from rfb_logger_tool import sys_log_logger_get_module_logger, Logger
log: Logger = sys_log_logger_get_module_logger(__name__)

from rfb_scpi_sniffer       import DrvScpiSerialConfC
from rfb_driver_epc import DrvEpcDeviceC, DrvEpcDataC
from rfb_driver_ea  import DrvEaDeviceC, DrvEaDataC
from rfb_driver_rs  import DrvRsDeviceC, DrvRsDataC
from rfb_driver_bk import DrvBkDeviceC
from rfb_driver_bases import DrvBaseStatusC
from rfb_driver_bms import DrvBmsDeviceC
from rfb_driver_flow import DrvFlowDeviceC
from rfb_cycler_datatypes.cycler_data import (CyclerDataDeviceTypeE, CyclerDataDeviceC,
                                CyclerDataPwrLimitE, CyclerDataDeviceStatusC, CyclerDataExtMeasC,
                                CyclerDataGenMeasC, CyclerDataAllStatusC, CyclerDataDeviceStatusE,
                                CyclerDataPwrModeE)

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################

#######################              ENUMS               #######################

######################             CONSTANTS              ######################
from .context import DEFAULT_PERIOD_ELECT_MEAS, DEFAULT_PERIOD_TEMP_MEAS
#######################             CLASSES              #######################

class MidDabsIncompatibleActionErrorC(Exception):
    """Exception raised when the action is not compatible with the device.
    """
    def __init__(self, message: str) -> None:
        """Exception raised fro erros when an action is not compatible with the device, and it is
        tried to be set.

        Args:
            message ([str]): [Explanation of the error]
        """
        super().__init__(message)

class MidDabsExtraMeterC:
    """Instanciates an objects that are only able to measures.
    """
    def __init__(self, device: CyclerDataDeviceC) -> None:
        self.device    :  DrvBmsDeviceC| DrvFlowDeviceC | DrvBkDeviceC |None = None # DrvBkDeviceC |
        self._dev_db_id : int = device.dev_db_id
        if device.mapping_names is None:
            self.__mapping_attr = {}
        else:
            self.__mapping_attr = device.mapping_names
        if device.device_type is CyclerDataDeviceTypeE.BMS:
            can_id= 0
            if isinstance(device.iface_name, str):
                can_id = int(device.iface_name,16)
            else:
                can_id = int(device.iface_name)
            self.device : DrvBmsDeviceC = DrvBmsDeviceC(can_id= can_id)
        elif device.device_type is CyclerDataDeviceTypeE.FLOW:
            self.device : DrvFlowDeviceC = DrvFlowDeviceC(
                            config= DrvScpiSerialConfC(port= device.iface_name,
                                                        **device.link_conf.__dict__),
                            rx_chan_name= "RX_SCPI_"+str(self._dev_db_id))
        elif device.device_type is CyclerDataDeviceTypeE.BK:
            self.device : DrvBkDeviceC = DrvBkDeviceC(
                                    DrvScpiSerialConfC(port= device.iface_name,
                                                        **device.link_conf.__dict__))

    def update(self, ext_meas: CyclerDataExtMeasC, status: CyclerDataAllStatusC) -> None:
        """Update the external measurements from bms or bk data.

        Args:
            ext_meas (CyclerDataExtMeasC): [description]
        """
        res = None
        res= self.device.get_data()
        if hasattr(res, 'status'):
            if isinstance(res.status, DrvBaseStatusC):
                state = CyclerDataDeviceStatusC(error= getattr(res,'status').error_code,
                                                    dev_db_id= self._dev_db_id)
                setattr(status, 'extra_meter_'+str(self._dev_db_id), state)
        elif isinstance(self.device, DrvBkDeviceC):
            bk_state = CyclerDataDeviceStatusC(error= res.status.error_code,
                                                dev_db_id= self._dev_db_id)
            setattr(status, 'extra_meter_'+str(self._dev_db_id), bk_state)
        for key in self.__mapping_attr.keys():
            setattr(ext_meas, key+'_'+str(self.__mapping_attr[key]),
                    getattr(res, key))

    def close(self):
        """Close connection with the device"""
        try:
            self.device.close()
        except Exception as err:
            log.error(f"Error while closing device: {err}")
            raise Exception("Error while closing device") from err #pylint: disable= broad-exception-raised

class MidDabsPwrMeterC: #pylint: disable= too-many-instance-attributes
    '''Instanciates an object enable to measure but are also power devices.
    '''
    def __init__(self, device: list [CyclerDataDeviceC]) -> None: #pylint: disable= too-many-branches
        pwr_devices: List[CyclerDataDeviceC] = device.copy()
        for dev in pwr_devices:
            if not dev.is_control:
                log.debug(f"Removing... {dev.device_type}")
                pwr_devices.remove(dev)
        self.device_type: CyclerDataDeviceTypeE = pwr_devices[0].device_type
        self._dev_db_id: List = [p_device.dev_db_id for p_device in pwr_devices]
        ## Device id in database when using source-load will always be first source and then load
        if len(pwr_devices) > 1:
            if pwr_devices[0].device_type is CyclerDataDeviceTypeE.SOURCE:
                self._dev_db_id = [pwr_devices[0].dev_db_id, pwr_devices[1].dev_db_id]
            else:
                self._dev_db_id = [pwr_devices[1].dev_db_id, pwr_devices[0].dev_db_id]

        ## Commented for first version
        self.bisource   : DrvEaDeviceC | None = None
        self.source     : DrvEaDeviceC | None = None
        self.load       : DrvRsDeviceC | None = None
        self.epc        : DrvEpcDeviceC| None = None
        try:
            for dev in pwr_devices:
                if dev.device_type == CyclerDataDeviceTypeE.EPC:
                    can_id= 0
                    if not dev.iface_name.isnumeric(): # isinstance(dev.iface_name, str),
                        can_id = int(dev.iface_name,16)
                    else:
                        can_id = int(dev.iface_name)
                    self.epc : DrvEpcDeviceC = DrvEpcDeviceC(can_id=can_id) #pylint: disable= unexpected-keyword-arg, no-value-for-parameter
                    self.epc.open()
                    self.mapping_epc = dev.mapping_names
                    self.epc.set_periodic(ack_en = False,
                        elect_en = True, elect_period = DEFAULT_PERIOD_ELECT_MEAS,
                        temp_en = True, temp_period = DEFAULT_PERIOD_TEMP_MEAS)
                elif dev.device_type is CyclerDataDeviceTypeE.SOURCE:
                    self.source : DrvEaDeviceC = DrvEaDeviceC(
                                    DrvScpiSerialConfC(port= dev.iface_name,
                                                        **dev.link_conf.__dict__))
                    self.mapping_source = dev.mapping_names
                elif dev.device_type is CyclerDataDeviceTypeE.LOAD:
                    # TODO: Update SCPI not needing handler
                    self.load : DrvRsDeviceC = DrvRsDeviceC(
                                    DrvScpiSerialConfC(port= dev.iface_name,
                                                        **dev.link_conf.__dict__))
                    self.mapping_load = dev.mapping_names
                elif self.device_type is CyclerDataDeviceTypeE.BISOURCE:
                    self.bisource : DrvEaDeviceC = DrvEaDeviceC(
                                DrvScpiSerialConfC(port= dev.iface_name,
                                                    **dev.link_conf.__dict__))
                    self.mapping_bisource = dev.mapping_names
                else:
                    log.error(f"The dessire device doesn't have type {self.device_type}")
        except Exception as error:
            log.error(error)
            raise error

    def __update_source_load_status(self, status: CyclerDataAllStatusC):
        if status.source != CyclerDataDeviceStatusE.OK:
            status.pwr_dev = status.source
        elif status.load != CyclerDataDeviceStatusE.OK:
            status.pwr_dev = status.load
        else:
            status.pwr_dev = status.source

    def update(self, gen_meas: CyclerDataGenMeasC, ext_meas: CyclerDataExtMeasC,#pylint: disable= too-many-branches, too-many-statements
               status: CyclerDataAllStatusC) -> None:
        """Update the data from the hardware sendind the corresponding messages.
        Update the variables of the class with the data received from the device.
        Depending on the device type, the data will be updated in a way or another.
        """
        if self.device_type is CyclerDataDeviceTypeE.EPC:
            msg_elect_meas = self.epc.get_elec_meas(periodic_flag= True)
            msg_temp_meas = self.epc.get_temp_meas(periodic_flag= True)
            msg_mode: DrvEpcDataC  = self.epc.get_mode()
            epc_status = self.epc.get_status()
            status.pwr_dev = CyclerDataDeviceStatusC(error= epc_status.error_code,
                                                    dev_db_id= self._dev_db_id[0]) #pylint: disable= no-member
            gen_meas.voltage = msg_elect_meas.ls_voltage
            gen_meas.current = msg_elect_meas.ls_current
            gen_meas.power   = msg_elect_meas.ls_power
            ## There is no error mode in cycler device mode
            if msg_mode.mode.value == 5:
                pwr_mode = CyclerDataPwrModeE.WAIT
            else:
                pwr_mode = CyclerDataPwrModeE(msg_mode.mode.value)
            status.pwr_mode = pwr_mode
            if self.mapping_epc is not None:
                for key in self.mapping_epc.keys():
                    if 'temp' in key:
                        setattr(ext_meas, key+'_'+str(self.mapping_epc[key]),
                                getattr(msg_temp_meas, key))
                    else:
                        setattr(ext_meas, key+'_'+str(self.mapping_epc[key]),
                                getattr(msg_elect_meas, key))
        elif self.device_type is CyclerDataDeviceTypeE.BISOURCE:
            res_bisource: DrvEaDataC = self.bisource.get_data()
            status.pwr_dev = CyclerDataDeviceStatusC(error= res_bisource.status.error_code,
                                                    dev_db_id= self._dev_db_id[0])
            gen_meas.voltage = res_bisource.voltage
            gen_meas.current = res_bisource.current
            gen_meas.power   = res_bisource.power
            status.pwr_mode = CyclerDataPwrModeE(res_bisource.mode.value)
        elif self.device_type in (CyclerDataDeviceTypeE.SOURCE, CyclerDataDeviceTypeE.LOAD):
            res_source: DrvEaDataC = self.source.get_data()
            status.source = CyclerDataDeviceStatusC(error= res_source.status.error_code,
                                            dev_db_id= self._dev_db_id[0])
            res_load: DrvRsDataC = self.load.get_data()
            status.load = CyclerDataDeviceStatusC(error= res_load.status.error_code,
                                            dev_db_id= self._dev_db_id[1])
            log.debug(f"Source mode: {res_source.mode.name}, {res_source.mode.value}")
            log.debug(f"Load mode: {res_load.mode.name}, {res_load.mode.value}")
            if res_source.power >= res_load.power:
                gen_meas.voltage = res_load.voltage
                gen_meas.current = res_source.current
                gen_meas.power   = res_source.power
                status.pwr_mode = CyclerDataPwrModeE(res_source.mode.value)
            else:
                gen_meas.voltage = res_load.voltage
                # The current is negative because the load is consuming power
                gen_meas.current = res_load.current*-1
                gen_meas.power   = res_load.power*-1
                status.pwr_mode = CyclerDataPwrModeE(res_load.mode.value)
            if res_source.mode.value == 0 and res_load.mode.value == 4:
                status.pwr_mode = CyclerDataPwrModeE.WAIT
            if self.mapping_load is not None:
                for key in self.mapping_load.keys():
                    if 'power' in key or 'current' in key:
                        setattr(ext_meas, key+'_'+str(self.mapping_load[key]),
                                getattr(res_load, key)*-1)
                    else:
                        setattr(ext_meas, key+'_'+str(self.mapping_load[key]),
                                getattr(res_load, key))
            if self.mapping_source is not None:
                for key in self.mapping_source.keys():
                    setattr(ext_meas, key+'_'+str(self.mapping_source[key]),
                            getattr(res_source, key))
        if self.device_type in (CyclerDataDeviceTypeE.LOAD, CyclerDataDeviceTypeE.SOURCE):
            self.__update_source_load_status(status= status)

    def close(self):
        """Close connection in serial with the device"""
        try:
            if self.device_type is CyclerDataDeviceTypeE.EPC:
                self.epc.close()
            elif self.device_type is CyclerDataDeviceTypeE.BISOURCE:
                self.bisource.close()
            elif self.device_type in (CyclerDataDeviceTypeE.SOURCE, CyclerDataDeviceTypeE.LOAD):
                self.source.close()
                self.load.close()
        except Exception as err:
            log.error(f"Error while closing device: {err}")
            raise Exception("Error while closing device") from err #pylint: disable= broad-exception-raised

class MidDabsPwrDevC(MidDabsPwrMeterC):
    """Instanciates an object enable to control the devices.
    """
    def _init__(self, device: List[CyclerDataDeviceC])->None:
        super().__init__(device)

    def set_cv_mode(self,volt_ref: int, limit_ref: int|None = None,
                    limit_type: CyclerDataPwrLimitE|None = None,
                    actual_voltage: int|None = None,
                    actual_current: int|None = None) -> CyclerDataDeviceStatusE:
        """Set the CV mode with the given voltage and current limit.
        To set cv mode in epc must have argument limit_type
        Args:
            volt_ref (int): [voltage in mV]
            limit_ref (int): [limit reference, for the epc could be mA/dW/ms the rest of devices
                            is mA]
        """
        res = CyclerDataDeviceStatusE.OK
        if self.device_type is CyclerDataDeviceTypeE.EPC:
            try:
                self.epc.set_cv_mode(volt_ref,limit_type, limit_ref)
            except ValueError as err:
                log.error(f"Error while setting CV mode {err}")
                res = CyclerDataDeviceStatusE.INTERNAL_ERROR
        elif self.device_type is CyclerDataDeviceTypeE.BISOURCE:
            try:
                self.bisource.set_cv_mode(volt_ref, limit_ref)
            except ValueError as err:
                res = CyclerDataDeviceStatusE.INTERNAL_ERROR
                log.error(f"Error while setting CV mode {err}")
        elif self.device_type in (CyclerDataDeviceTypeE.SOURCE, CyclerDataDeviceTypeE.LOAD):
            if ((actual_voltage is not None and actual_voltage<volt_ref*1.1) and
                (actual_current is not None and actual_current>=0)):
                self.load.disable()
                try:
                    self.source.set_cv_mode(volt_ref, limit_ref)
                except ValueError as err:
                    log.error(f"Error while setting CV mode {err}")
                    raise err
            else:
                # TODO: upgrade DrvRs to write limits when setting modes
                # This todo is not possible, the load device doesn't allow to set limits
                self.source.disable()
                self.load.set_cv_mode(volt_ref)
        else:
            log.warning("This device is not able to change to CV mode.")
            raise MidDabsIncompatibleActionErrorC(("This device is not able to change to "
                                                    "CV mode."))
        return res

    def set_cc_mode(self, current_ref: int, limit_ref: int|None= None,
                    limit_type: CyclerDataPwrLimitE|None = None) -> CyclerDataDeviceStatusE:
        """Set the CC mode with the given current and voltage limit.
            To set cc mode in epc must have argument limit_type
        Args:
            current_ref (int): [current in mA]
            limit_ref (int): [limit reference, for the epc could be mV/dW/ms the rest of devices
                            is mV]
        """
        res = CyclerDataDeviceStatusE.OK
        if self.device_type is CyclerDataDeviceTypeE.EPC:
            try:
                self.epc.set_cc_mode(ref= current_ref, limit_type= limit_type, limit_ref= limit_ref)
            except ValueError as err:
                log.error(f"Error while setting CC mode {err}")
                res = CyclerDataDeviceStatusE.INTERNAL_ERROR
        elif self.device_type is  CyclerDataDeviceTypeE.BISOURCE:
            self.bisource.set_cc_mode(current_ref, limit_ref)
        elif self.device_type in (CyclerDataDeviceTypeE.SOURCE, CyclerDataDeviceTypeE.LOAD):
            if current_ref>0:
                self.load.disable()
                self.source.set_cc_mode(current_ref, limit_ref)
            else:
                # TODO: upgrade DrvRs to write limits when setting modes
                # This todo is not possible, the load device doesn't allow to set limits
                self.source.disable()
                self.load.set_cc_mode(abs(current_ref))
        else:
            log.warning("This device is not able to change to CC modes.")
            raise MidDabsIncompatibleActionErrorC(("This device is not able to change to "
                                                    "CC modes."))
        return res

    def set_cp_mode(self, pwr_ref: int, limit_type: CyclerDataPwrLimitE,
                    limit_ref: int) -> CyclerDataDeviceStatusE:
        """Set the CP mode with the specified limits, only possible in the epc.

        Args:
            pwr_ref (int): [description]
            limit_type (CyclerDataPwrLimitE): [description]
            limit_ref (int): [description]
        """
        res = CyclerDataDeviceStatusE.OK
        if self.device_type is CyclerDataDeviceTypeE.EPC:
            try:
                self.epc.set_cp_mode(pwr_ref, limit_type, limit_ref)
            except ValueError as err:
                log.error(f"Error while setting CP mode {err}")
                res = CyclerDataDeviceStatusE.INTERNAL_ERROR
        else:
            log.error('This device is incompatible with power control mode')
            raise MidDabsIncompatibleActionErrorC(("This device is incompatible with "
                                                    "power control mode"))
        return res

    def set_wait_mode(self, time_ref: int = 0) -> CyclerDataDeviceStatusE:
        """Set the wait mode for the device.
        To set the wait mode in epc must write argument time_ref = number_in_ms
        """
        res = CyclerDataDeviceStatusE.OK
        if self.device_type is CyclerDataDeviceTypeE.EPC:
            try:
                self.epc.set_wait_mode(limit_ref = time_ref) #pylint: disable= no-value-for-parameter
            except ValueError as err:
                log.error(f"Error while setting WAIT mode {err}")
                res = CyclerDataDeviceStatusE.INTERNAL_ERROR
        else:
            if self.device_type in (CyclerDataDeviceTypeE.SOURCE, CyclerDataDeviceTypeE.LOAD):
                self.source.set_wait_mode()
                self.load.set_wait_mode()
            else:
                self.bisource.set_wait_mode()
        return res

    def set_limits(self, ls_volt: tuple | None = None, ls_curr: tuple | None = None,
                   ls_pwr: tuple | None = None, hs_volt: tuple | None = None,
                   temp: tuple | None = None) -> CyclerDataDeviceStatusE:
        """Set the limits of the ECP.

        Args:
            ls_volt (tuple, optional): [max_value, min_value]. Defaults to None.
            ls_curr (tuple, optional): [max_value, min_value]. Defaults to None.
            ls_pwr (tuple, optional): [max_value, min_value]. Defaults to None.
            hs_volt (tuple, optional): [max_value, min_value]. Defaults to None.
            temp (tuple, optional): [max_value, min_value]. Defaults to None.
        """
        res = CyclerDataDeviceStatusE.OK
        if self.device_type is CyclerDataDeviceTypeE.EPC:
            try:
                if isinstance(ls_curr, tuple):
                    self.epc.set_ls_curr_limit(ls_curr[0], ls_curr[1])
                if isinstance(ls_volt, tuple):
                    self.epc.set_ls_volt_limit(ls_volt[0], ls_volt[1])
                if isinstance(ls_pwr, tuple):
                    self.epc.set_ls_pwr_limit(ls_pwr[0], ls_pwr[1])
                if isinstance(hs_volt, tuple):
                    self.epc.set_hs_volt_limit(hs_volt[0], hs_volt[1])
                if isinstance(temp, tuple):
                    self.epc.set_temp_limit(temp[0], temp[1])
            except ValueError as err:
                log.error(f"Error while setting limits {err}")
                res = CyclerDataDeviceStatusE.INTERNAL_ERROR
        else:
            log.error("The limits can not be change in this device")
            raise MidDabsIncompatibleActionErrorC("The limits can not be change in this device")
        return res

    def disable(self) -> CyclerDataDeviceStatusE:
        """Disable the devices.
        """
        if self.device_type is CyclerDataDeviceTypeE.EPC:
            log.info("Disabling epc")
            self.epc.disable()
        elif self.device_type is CyclerDataDeviceTypeE.BISOURCE:
            self.bisource.disable()
        elif self.device_type in [CyclerDataDeviceTypeE.SOURCE, CyclerDataDeviceTypeE.LOAD]:
            log.info("Disabling source")
            self.source.disable()
            log.info("Disabling load")
            self.load.disable()
        else:
            log.error("The device can not be disable")
            raise MidDabsIncompatibleActionErrorC("The device can not be disable")
