from unrealcv.automation import UE4Binary
from unrealcv.util import read_png, read_npy
from unrealcv import client

class IXRay:
    """Informal interface for different types of x-rays."""

    def __init__(self):
        self.position = [0.0, 0.0, 0.0, 0.0]

    def connect(self) -> str:
        """Connect to the x-ray"""
        return "Connection failed: Not implemented!"

    def move(self, position) -> str:
        """Move x-ray to position"""
        return "Move failed: Not implemented!"

    def capture(self) -> str:
        """Get an image from the x-ray. Returns the file path"""
        return "Capture failed: Not implemented!"

    @property
    def position(self):
        """:obj:'list' of :obj:'float': Position of the x-ray: [x, y, z, phi]

        x:   [0,1]   from top to bottom (if patient is lying down: typically left to right)
        y:   [0,1]   up / down
        z:   [0,1]   closing in to patient
        phi: [0,360] ° rotation around patient, 0 is level on the side of the surgeon
        """
        return self._position

    @position.setter
    def position(self, position):
        self._position = position


class UE4XRay(IXRay):
    """Simulated x-ray, using Unreal Engine 4 and UnrealCV"""



    def __init__(self):
        self.position = [0.5, 0.0, 0.0, 45]
        self._binary_path = ""

    def start_xray(self, binary_path) -> str:
        import os
        _binary_path = binary_path
        if os.path.isfile(_binary_path):
            # Use .exe file for windows.
            binary = UE4Binary(_binary_path)  # UE4Binary can support exe, linux and mac binary
            binary.start()
            return "X-ray start success: UE4 x-ray app started"
        else:
            return "X-ray start failure: Can not find binary file %s \nWorking directory is %s" % (binary_path, os.path.abspath('.'))

    def connect(self, binary_path) -> str:
        res_startup = self.start_xray(binary_path) + "\n"
        res_connect = client.connect() + "\n"
        return res_startup + res_connect + client.request("vget /unrealcv/version") + client.request("vget /unrealcv/status")

    def move(self, position) -> str:
        client.request("vset /unreal")
        return "Move success: new position is " + self._position



