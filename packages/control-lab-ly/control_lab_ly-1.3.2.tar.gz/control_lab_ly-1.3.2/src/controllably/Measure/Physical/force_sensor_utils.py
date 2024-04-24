# %% -*- coding: utf-8 -*-
"""
This module holds the class for force sensors.

Classes:
    ForceSensor (Measurer)

Other constants and variables:
    CALIBRATION_FACTOR (float)
    COLUMNS (tuple)
"""
# Standard library imports
from datetime import datetime
import pandas as pd
from threading import Thread
import time

# Third party imports
import serial # pip install pyserial

# Local application imports
from ..measure_utils import Measurer
print(f"Import: OK <{__name__}>")

CALIBRATION_FACTOR = 6.862879436681862  # FIXME: needs to be calibrated
"""Empirical factor by which to divide output reading by to get force in newtons"""
COLUMNS = ('Time', 'Value', 'Factor', 'Baseline', 'Force')
"""Headers for output data from force sensor"""

class ForceSensor(Measurer):
    """
    ForceSensor provides methods to read out values from a force sensor

    ### Constructor
    Args:
        `port` (str): COM port address
        `calibration_factor` (float, optional): calibration factor of device readout to newtons. Defaults to CALIBRATION_FACTOR.
    
    ### Attributes
    - `baseline` (float): baseline readout at which zero newtons is set
    - `calibration_factor` (float): calibration factor of device readout to newtons
    - `precision` (int): number of decimal places to print force value
    
    ### Properties
    - `force` (float): force experienced
    
    ### Methods
    - `clearCache`: clear most recent data and configurations
    - `disconnect`: disconnect from device
    - `getForce`: get the force response
    - `reset`: reset the device
    - `shutdown`: shutdown procedure for tool
    - `tare`: alias for `zero()`
    - `toggleFeedbackLoop`: start or stop feedback loop
    - `toggleRecord`: start or stop data recording
    - `zero`: set the current reading as baseline (i.e. zero force)
    """
    
    _default_flags = {
        'busy': False,
        'connected': False,
        'get_feedback': False,
        'pause_feedback': False,
        'read': True,
        'record': False
    }
    def __init__(self, port:str, calibration_factor:float = CALIBRATION_FACTOR, **kwargs):
        """
        Instantiate the class

        Args:
            port (str): COM port address
            calibration_factor (float, optional): calibration factor of device readout to newtons. Defaults to CALIBRATION_FACTOR.
        """
        super().__init__(**kwargs)
        self.baseline = 0
        self.buffer_df = pd.DataFrame(columns=COLUMNS)
        self.calibration_factor = calibration_factor
        self.precision = 3
        self._force = 0
        self._threads = {}
        self._connect(port)
        return
    
    # Properties
    @property
    def force(self) -> float:
        return round(self._force, self.precision)
   
    def clearCache(self):
        """Clear most recent data and configurations"""
        self.setFlag(pause_feedback=True)
        time.sleep(0.1)
        self.buffer_df = pd.DataFrame(columns=COLUMNS)
        self.setFlag(pause_feedback=False)
        return
    
    def disconnect(self):
        """Disconnect from device"""
        try:
            self.device.close()
        except Exception as e:
            if self.verbose:
                print(e)
        self.setFlag(connected=False)
        return
    
    def getForce(self) -> str:
        """
        Get the force response
        
        Returns:
            str: device response
        """
        response = self._read()
        now = datetime.now()
        try:
            value = int(response)
        except ValueError:
            pass
        else:
            self._force = (value - self.baseline) / self.calibration_factor
            if self.flags['record']:
                values = [
                    now, 
                    value, 
                    self.calibration_factor, 
                    self.baseline, 
                    self._force
                ]
                row = {k:v for k,v in zip(COLUMNS, values)}
                new_row_df = pd.DataFrame(row, index=[0])
                self.buffer_df = pd.concat([self.buffer_df, new_row_df], ignore_index=True)
        return response
  
    def reset(self):
        """Reset the device"""
        super().reset()
        self.baseline = 0
        return
    
    def shutdown(self):
        """Shutdown procedure for tool"""
        self.toggleFeedbackLoop(on=False)
        return super().shutdown()
 
    def tare(self):
        """Alias for `zero()`"""
        return self.zero()
    
    def toggleFeedbackLoop(self, on:bool):
        """
        Start or stop feedback loop

        Args:
            on (bool): whether to start loop to continuously read from device
        """
        self.setFlag(get_feedback=on)
        if on:
            if 'feedback_loop' in self._threads:
                self._threads['feedback_loop'].join()
            thread = Thread(target=self._loop_feedback)
            thread.start()
            self._threads['feedback_loop'] = thread
        else:
            self._threads['feedback_loop'].join()
        return
    
    def toggleRecord(self, on:bool):
        """
        Start or stop data recording

        Args:
            on (bool): whether to start recording data
        """
        self.setFlag(record=on, get_feedback=on, pause_feedback=False)
        self.toggleFeedbackLoop(on=on)
        return

    def zero(self, wait:int = 5):
        """
        Set current reading as baseline (i.e. zero force)
        
        Args:
            wait (int, optional): duration to wait while zeroing, in seconds. Defaults to 5.
        """
        if self.flags['record']:
            print("Unable to zero while recording.")
            print("Use `toggleRecord(False)` to stop recording.")
            return
        temp_record_state = self.flags['record']
        temp_buffer_df = self.buffer_df.copy()
        self.reset()
        self.toggleRecord(True)
        print(f"Zeroing... ({wait}s)")
        time.sleep(wait)
        self.toggleRecord(False)
        self.baseline = self.buffer_df['Value'].mean()
        self.clearCache()
        self.buffer_df = temp_buffer_df.copy()
        print("Zeroing complete.")
        self.toggleRecord(temp_record_state)
        return

    # Protected method(s)
    def _connect(self, port:str, baudrate:int = 115200, timeout:int = 1):
        """
        Connection procedure for tool

        Args:
            port (str): COM port address
            baudrate (int, optional): baudrate. Defaults to 115200.
            timeout (int, optional): timeout in seconds. Defaults to 1.
        """
        self.connection_details = {
            'port': port,
            'baudrate': baudrate,
            'timeout': timeout
        }
        device = None
        try:
            device = serial.Serial(port, baudrate, timeout=timeout)
        except Exception as e:
            print(f"Could not connect to {port}")
            if self.verbose:
                print(e)
        else:
            self.device = device
            print(f"Connection opened to {port}")
            self.setFlag(connected=True)
            time.sleep(1)
            self.zero()
        return
    
    def _loop_feedback(self):
        """Loop to constantly read from device"""
        print('Listening...')
        while self.flags['get_feedback']:
            if self.flags['pause_feedback']:
                continue
            self.getForce()
        print('Stop listening...')
        return

    def _read(self) -> str:
        """
        Read response from device

        Returns:
            str: response string
        """
        response = ''
        try:
            response = self.device.readline()
        except Exception as e:
            if self.verbose:
                print(e)
        else:
            response = response.decode('utf-8').strip()
            if self.verbose:
                print(response)
        return response
 