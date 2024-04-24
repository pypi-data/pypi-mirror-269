# %% -*- coding: utf-8 -*-
"""
This module holds the base class for movement tools from Dobot.

Classes:
    Dobot (RobotArm)

Other types:
    Device (namedtuple)

Other constants and variables:
    MOVE_TIME_BUFFER_S (float) = 0.5
"""
# Standard library imports
from __future__ import annotations
from collections import namedtuple
import ipaddress
import numpy as np
import socket
import time
from typing import Optional, Protocol

# Local application imports
from ....misc import Factory, Helper
from ..jointed_utils import RobotArm
from .dobot_api import dobot_api_dashboard, dobot_api_feedback
print(f"Import: OK <{__name__}>")

MOVE_TIME_BUFFER_S = 0.5

Device = namedtuple('Device', ['dashboard', 'feedback'])
"""Device is a named tuple for a dashboard,feedback pair"""

class DobotAttachment(Protocol):
    implement_offset: tuple
    def setDashboard(self, dashboard):
        ...

class Dobot(RobotArm):
    """
    Abstract Base Class (ABC) for Dobot objects. Dobot provides controls for articulated robots from Dobot.
    ABC cannot be instantiated, and must be subclassed with abstract methods implemented before use.
    
    ### Constructor
    Args:
        `ip_address` (str): IP address of Dobot
        `attachment_name` (str, optional): name of attachment. Defaults to None.
    
    ### Attributes
    - `attachment` (DobotAttachment): attached Dobot tool
    
    ### Properties
    - `dashboard` (dobot_api_dashboard): connection to status and signal control
    - `feedback` (dobot_api_feedback): connection to movement controls
    - `ip_address` (str): IP address of Dobot
    
    ### Methods
    #### Abstract
    - `isFeasible`: checks and returns whether the target coordinate is feasible
    #### Public
    - `calibrate`: calibrate the internal and external coordinate systems, then verify points
    - `disconnect`: disconnect from device
    - `getConfigSettings`: retrieve the robot's configuration
    - `moveCoordBy`: relative Cartesian movement and tool orientation, using robot coordinates
    - `moveCoordTo`: absolute Cartesian movement and tool orientation, using robot coordinates
    - `moveJointBy`: relative joint movement
    - `moveJointTo`: absolute joint movement
    - `reset`: reset the robot
    - `setSpeed`: set the speed of the robot
    - `shutdown`: shutdown procedure for tool
    - `stop`: halt robot movement
    - `toggleAttachment`: couple or remove Dobot attachment that interfaces with Dobot's digital output
    - `toggleCalibration`: enter or exit calibration mode, with a sharp point implement for alignment
    """
    
    _place: str = '.'.join(__name__.split('.')[1:-1])
    _default_move_time_buffer: float = MOVE_TIME_BUFFER_S
    def __init__(self, ip_address:str, attachment_name:str = None, **kwargs):
        """
        Instantiate the class

        Args:
            ip_address (str): IP address of Dobot
            attachment_name (str, optional): name of attachment. Defaults to None.
        """
        super().__init__(**kwargs)
        self.attachment = None
        self._speed_max = dict(general=100)
        
        self._connect(ip_address)
        if attachment_name is not None:
            attachment_class = Factory.get_class(attachment_name)
            self.toggleAttachment(True, attachment_class)
        pass
    
    # Properties
    @property
    def dashboard(self) -> dobot_api_dashboard:
        return self.device.dashboard
    
    @property
    def feedback(self) -> dobot_api_feedback:
        return self.device.feedback
    
    @property
    def ip_address(self) -> str:
        return self.connection_details.get('ip_address', '')
    
    def calibrate(self, 
        external_pt1:np.ndarray, 
        internal_pt1:np.ndarray, 
        external_pt2:np.ndarray, 
        internal_pt2:np.ndarray
    ):
        """
        Calibrate the internal and external coordinate systems, then verify points.

        Args:
            external_pt1 (np.ndarray): x,y,z coordinates of physical point 1
            internal_pt1 (np.ndarray): x,y,z coordinates of robot point 1
            external_pt2 (np.ndarray): x,y,z coordinates of physical point 2
            internal_pt2 (np.ndarray): x,y,z coordinates of robot point 2
        """
        super().calibrate(external_pt1, internal_pt1, external_pt2, internal_pt2)

        # Verify calibrated points
        for pt in [external_pt1, external_pt2]:
            self.home()
            self.moveTo( pt + np.array([0,0,10]) )
            input("Press Enter to verify reference point")
        self.home()
        return
    
    def disconnect(self):
        """Disconnect from device"""
        self.reset()
        try:
            self.dashboard.close()
            self.feedback.close()
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
        self.setFlag(connected=False)
        return
    
    def getConfigSettings(self, attributes:Optional[list[str]] = None) -> dict:
        """
        Retrieve the robot's configuration
        
        Args:
            attributes (list[str]): list of attributes to retrieve values from
        
        Returns:
            dict: dictionary of robot class and configuration
        """
        attributes = [
            "ip_address", 
            "home_coordinates", 
            "home_orientation", 
            "orientate_matrix", 
            "translate_vector", 
            "implement_offset",
            "scale"
        ] if attributes is None else attributes
        return super().getConfigSettings(attributes)

    @Helper.safety_measures
    def moveCoordBy(self, 
        vector: tuple[float] = (0,0,0), 
        angles: tuple[float] = (0,0,0),
        **kwargs
    ) -> bool:
        """
        Relative Cartesian movement and tool orientation, using robot coordinates

        Args:
            vector (tuple[float], optional): x,y,z displacement vector. Defaults to (0,0,0).
            angles (tuple[float], optional): a,b,c rotation angles in degrees. Defaults to (0,0,0).

        Returns:
            bool: whether movement is successful
        """
        vector = tuple(vector)
        angles = tuple(angles)
        try:
            self.feedback.RelMovL(*vector)
            self.rotateBy(angles)
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
            self.updatePosition(vector=vector, angles=angles)
            return False
        else:
            if kwargs.get('wait', True) and self.isConnected():
                coordinates = self.position[0] + np.array(vector)
                coord_rotations = self._convert_cartesian_to_angles(self.position[0], coordinates)
                rotations = np.array([*coord_rotations, *angles])
                angular_speeds = self.max_speeds * self.speed_factor
                
                move_time = self._get_move_wait_time(distances=rotations, speeds=angular_speeds)
                move_time *= 2
                move_time += self._move_time_buffer
                print(f'Move for {move_time}s...')
                time.sleep(move_time)
        self.updatePosition(vector=vector, angles=angles)
        return True

    @Helper.safety_measures
    def moveCoordTo(self, 
        coordinates: Optional[tuple[float]] = None, 
        orientation: Optional[tuple[float]] = None,
        **kwargs
    ) -> bool:
        """
        Absolute Cartesian movement and tool orientation, using robot coordinates

        Args:
            coordinates (Optional[tuple[float]], optional): x,y,z position vector. Defaults to None.
            orientation (Optional[tuple[float]], optional): a,b,c orientation angles in degrees. Defaults to None.
        
        Returns:
            bool: whether movement is successful
        """
        coordinates = self.coordinates if coordinates is None else coordinates
        orientation = self.orientation if orientation is None else orientation
        coordinates = tuple(coordinates)
        orientation = tuple(orientation)
        if len(orientation) == 1 and orientation[0] == 0:
            orientation = self.orientation
        if not self.isFeasible(coordinates):
            print(f"Infeasible coordinates! {coordinates}")
            return
        
        try:
            self.feedback.MovJ(*coordinates, *orientation)
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
            self.updatePosition(coordinates=coordinates, orientation=orientation)
            return False
        else:
            if kwargs.get('wait', True) and self.isConnected():
                angles = abs(self.position[1] - np.array(orientation))
                coord_rotations = self._convert_cartesian_to_angles(self.position[0], np.array(coordinates))
                rotations = np.array([*coord_rotations, *angles])
                angular_speeds = self.max_speeds * self.speed_factor
                
                move_time = self._get_move_wait_time(distances=rotations, speeds=angular_speeds)
                move_time *= 2
                move_time += self._move_time_buffer
                print(f'Move for {move_time}s...')
                time.sleep(move_time)
        self.updatePosition(coordinates=coordinates, orientation=orientation)
        return True

    @Helper.safety_measures
    def moveJointBy(self, relative_angles: tuple[float], **kwargs) -> bool:
        """
        Relative joint movement

        Args:
            relative_angles (tuple[float]): j1~j6 rotation angles in degrees

        Raises:
            ValueError: Length of input needs to be 6.

        Returns:
            bool: whether movement is successful
        """
        if len(relative_angles) != 6:
            raise ValueError('Length of input needs to be 6.')
        try:
            self.feedback.RelMovJ(*relative_angles)
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
            self.updatePosition(angles=relative_angles[3:])
            return False
        else:
            if kwargs.get('wait', True) and self.isConnected():
                rotations = abs(np.array(relative_angles))
                angular_speeds = self.max_speeds * self.speed_factor
                
                move_time = self._get_move_wait_time(distances=rotations, speeds=angular_speeds)
                move_time *= 2
                move_time += self._move_time_buffer
                print(f'Move for {move_time}s...')
                time.sleep(move_time)
        self.updatePosition(angles=relative_angles[3:])
        return True

    @Helper.safety_measures
    def moveJointTo(self, absolute_angles: tuple[float], **kwargs) -> bool:
        """
        Absolute joint movement

        Args:
            absolute_angles (tuple[float]): j1~j6 orientation angles in degrees

        Raises:
            ValueError: Length of input needs to be 6.

        Returns:
            bool: whether movement is successful
        """
        if len(absolute_angles) != 6:
            raise ValueError('Length of input needs to be 6.')
        try:
            self.feedback.JointMovJ(*absolute_angles)
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
            self.updatePosition(orientation=absolute_angles[3:])
            return False
        else:
            if kwargs.get('wait', True) and self.isConnected():
                rotations = abs(self.orientation - np.array(absolute_angles))
                angular_speeds = self.max_speeds * self.speed_factor
                
                move_time = self._get_move_wait_time(distances=rotations, speeds=angular_speeds)
                move_time *= 2
                move_time += self._move_time_buffer
                print(f'Move for {move_time}s...')
                time.sleep(move_time)
        self.updatePosition(orientation=absolute_angles[3:])
        return True

    def reset(self):
        """Reset the robot"""
        try:
            self.dashboard.DisableRobot()
            self.dashboard.ClearError()
            self.dashboard.EnableRobot()
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
        return
    
    def setSpeed(self, speed:float) -> tuple[bool, float]:
        """
        Set the speed of the robot (functionally equivalent to setting the speed fraction)

        Args:
            speed (int): rate value (value range: 1~100)
            
        Returns:
            tuple[bool, float]: whether speed was changed; prevailing speed
        """
        ret,_ = self.setSpeedFactor(speed/100)
        return ret, self.speed
    
    def setSpeedFactor(self, speed_factor:float) -> tuple[bool, float]:
        """
        Set the speed fraction of the robot

        Args:
            speed_factor (int): fraction of maximum speed (value range: 0~1)
        
        Returns:
            tuple[bool, float]: whether speed was changed; prevailing speed fraction
        """
        if speed_factor == self.speed_factor:
            return False, self.speed_factor
        speed_factor = self.speed_factor if speed_factor is None else speed_factor
        prevailing_speed_factor = self.speed_factor
        try:
            self.dashboard.SpeedFactor(int(100*max(0.01,min(1,speed_factor))))
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
            return False, self.speed_factor
        self._speed_factor = speed_factor
        return True, prevailing_speed_factor
    
    def shutdown(self):
        """Shutdown procedure for tool"""
        self._freeze()
        return super().shutdown()
    
    def stop(self):
        """Halt robot movement"""
        try:
            self.dashboard.ResetRobot()
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
        return
    
    def toggleAttachment(self, on:bool, attachment_class:Optional[DobotAttachment] = None, channel_map:Optional[dict] = None):
        """
        Couple or remove Dobot attachment that interfaces with Dobot's digital output

        Args:
            on (bool): whether to couple Dobot attachment
            attachment_class (Optional[DobotAttachment], optional): Dobot attachment to couple. Defaults to None.
            channel_map (Optional[dict], optional): mapping of digital I/O channel(s). Defaults to None.
        """
        if on: # Add attachment
            print("Please secure tool attachment.")
            self.attachment: DobotAttachment = attachment_class(dashboard=self.dashboard, channel_map=channel_map)
            self.setImplementOffset(self.attachment.implement_offset)
        else: # Remove attachment
            print("Please remove tool attachment.")
            self.attachment = None
            self.setImplementOffset((0,0,0))
        return
    
    def toggleCalibration(self, on:bool, tip_length:float):
        """
        Enter or exit calibration mode, with a sharp point implement for alignment

        Args:
            on (bool): whether to set to calibration mode
            tip_length (int, optional): length of sharp point alignment implement
        """
        if on: # Enter calibration mode
            input(f"Please swap to calibration tip.")
            self._temporary_tool_offset = self.implement_offset
            self.setImplementOffset((0,0,-tip_length))
        else: # Exit calibration mode
            input("Please swap back to original tool.")
            self.setImplementOffset(self._temporary_tool_offset)
            del self._temporary_tool_offset
        return

    # Protected method(s)
    def _connect(self, ip_address:str, timeout:int = 10):
        """
        Connection procedure for tool

        Args:
            ip_address (str): IP address of robot
            timeout (int, optional): duration to wait before timeout. Defaults to 10.
        """
        self.connection_details = {
            'ip_address': ip_address,
            'timeout': timeout
        }
        self.device = Device(None,None)
        
        # Check if machine is connected to the same network as device
        hostname = socket.getfqdn()
        local_ip = socket.gethostbyname_ex(hostname)[2][0]
        local_network = f"{'.'.join(local_ip.split('.')[:-1])}.0/24"
        if ipaddress.ip_address(ip_address) not in ipaddress.ip_network(local_network):
            print(f"Current IP Network: {local_network[:-3]}")
            print(f"Device  IP Address: {ip_address}")
            return
        
        try:
            start_time = time.perf_counter()
            dashboard = dobot_api_dashboard(ip_address, 29999)
            if time.perf_counter() - start_time > timeout:
                raise Exception(f"Unable to connect to arm at {ip_address}")
            
            start_time = time.perf_counter()
            feedback = dobot_api_feedback(ip_address, 30003)
            if time.perf_counter() - start_time > timeout:
                raise Exception(f"Unable to connect to arm at {ip_address}")
        except Exception as e:
            print(e)
        else:
            self.device = Device(dashboard, feedback)
            self.reset()
        
        try:
            self.dashboard.User(0)
            self.dashboard.Tool(0)
        except OSError as e:
            print(e)
        except AttributeError as e:
            print(e)
        else:
            self.setSpeedFactor(1)
            self.setFlag(connected=True)
        return

    def _freeze(self):
        """Halt and disable robot"""
        try:
            self.dashboard.ResetRobot()
            self.dashboard.DisableRobot()
        except (AttributeError, OSError):
            if self.verbose:
                print("Not connected to arm.")
        return
