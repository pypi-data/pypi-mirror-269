"""In a typical workflow, these objects are automatically created by initializing the ["ASetup"][asmu.AFile] class.
The objects can be accessed by the attributes ["interface"][asmu.ASetup.interface], ["inputs"][asmu.ASetup.inputs] and ["outputs"][asmu.ASetup.outputs].
This page is an overview of the attributes one can set/get for the different objects."""
import numpy as np
import sounddevice as sd
from typing import List, Tuple, Callable

DEBUG = True

def query_devices() -> sd.DeviceList:
        """List all connected audio devices.

        Returns:
            sd.DeviceList: A DeviceList containing one dictionary for each available device.
        """
        return sd.query_devices()

class IO():
    def __init__(self, io_setup: dict) -> None:
        """Parent class for Input and Output configuration, storing various attributes.

        Args:
            io_setup (dict): ASetup input or output settings.
        """
        self._io_setup = io_setup

    def __repr__(self):
        return self.name

    @property
    def name(self) -> str:
        """IO name."""
        return self._io_setup["name"]

    @property
    def channel(self) -> int:
        """IO channel number (starting from 1)."""
        return int(self._io_setup["channel"])

    @property
    def color(self) -> str:
        """IO color in HEX format"""
        return self._io_setup["color"]
    @color.setter
    def color(self, value: str) -> None:
        self._io_setup["color"] = str(value)
    
    @property
    def pos(self) -> np.ndarray:
        """IO spacial coordinates in [1, 2, 3]"""
        return np.array(self._io_setup["pos"])
    @pos.setter
    def pos(self, value: np.ndarray) -> None:
        self._io_setup["pos"] = value.tolist()

    @property
    def reference(self) -> bool:
        """Reference flag, if no flag is found return `False`."""
        try:
            return bool(self._io_setup["reference"])
        except KeyError:
            return False
    @reference.setter
    def reference(self, value: bool) -> None:
        if value:
            self._io_setup["reference"] = True
        else:
            try:
                del self._io_setup["reference"]
            except KeyError:
                pass

    @property
    def io_setup(self):
        """IO setup dictionary used in ASetup files."""
        return self._io_setup
    
    # CALIBRATION FACTORS - defined by amplitude -> direct signal conversion!
    @property
    def cPa(self) -> float:
        """Calibration factor to covert the arbitrary unit to Pascal (Pa)."""
        return float(self._io_setup["cPa"])
    @cPa.setter
    def cPa(self, value: float) -> None:
        self._io_setup["cPa"] = float(value)

    @property
    def kPa(self) -> float:
        """Discrete calibration frequency of cPa calibration."""
        return int(self._io_setup["kPa"])
    @kPa.setter
    def kPa(self, value: float) -> None:
        self._io_setup["kPa"] = float(value)

    @property
    def cV(self) -> float:
        """Calibration factor to covert the arbitrary unit to Volt (V)."""
        return float(self._io_setup["cV"])
    @cV.setter
    def cV(self, value: float) -> None:
        self._io_setup["cV"] = float(value)

    @property
    def kV(self) -> float:
        """Discrete calibration frequency of cV calibration."""
        return float(self._io_setup["kV"])
    @kV.setter
    def kV(self, value: float) -> None:
        self._io_setup["kV"] = float(value)

    @property
    def cFR(self) -> np.ndarray:
        """Discrete frequency response calibration vector."""
        return self._io_setup["cFR"]
    @cFR.setter
    def cFR(self, value: np.ndarray) -> None:
        self._io_setup["cFR"] = np.array(value)


class Input(IO):
    def __init__(self, input_setup: dict) -> None: 
        """Input class, typically automatically created when ASetup is initialized.

        Args:
            input_setup (dict): ASetup input settings.
        """
        self._input_setup = input_setup
        super().__init__(self._input_setup)


class Output(IO):
    def __init__(self, output_setup: dict) -> None: 
        """Output class, typically automatically created when ASetup is initialized.

        Args:
            output_setup (dict): ASetup output settings.
        """
        self._output_setup = output_setup
        super().__init__(self._output_setup)


class Interface():
    def __init__(self, interface_setup: dict) -> None:
        """Class for audio interface communication and settings.

        Args:
            interface_setup (dict): ASetup interface settings.
        """
        self._interface_setup = interface_setup

    @property
    def name(self) -> None:
        """Interface name"""
        return self._interface_setup["name"]

    @property
    def device(self):
        """Device name obtained by [`queury_devices()`][asmu.io.query_devices]."""
        return self._interface_setup["device"]
    @device.setter
    def device(self, value):
        self._interface_setup["device"] = value

    @property
    def samplerate(self):
        """Samplerate"""
        return int(self._interface_setup["samplerate"])

    @property
    def blocksize(self) -> int:
        """Blocksize to use for interface communication (should be a power of 2).
            - Lower blocksize -> Reduces latency, but increases CPU load.
            - Higher blocksize -> Increases latency, but reduces CPU load.
        Typical values are between 32 and 8192."""
        return int(self._interface_setup['blocksize'])

    # SOUNDDEVICE 
    def _init_sounddevice(self, io:Tuple[List[Input], List[Output]]) -> None:
        """Initiializes sounddevice with the classes attributes for the given lists of inputs and outputs.
        !!! warning
            This method is currently only implemented for ASIO devices (Windows).
    
        Args:
            io (tuple of lists): Tuple that contains lists of Input and Output objects.
                If one of them is not needed, leave list empty.

        Raises:
            AttributeError: No audio device specified
        """
        sd.default.samplerate = self.samplerate
        sd.default.dtype = np.float32
        sd.default.blocksize = self.blocksize
        try:
            sd.default.device = self.device # TODO - different input and output device
        except KeyError:
            raise AttributeError("No audio device specified")

        if "ASIO" in self.device:
            if io[0]:
                in_channels = [input.channel - 1 for input in io[0]] # convert to channel names starting with 0
                asio_in = sd.AsioSettings(channel_selectors=in_channels)

                if not io[1]:
                    sd.default.extra_settings = asio_in
                    sd.default.channels = len(in_channels)
                    return

            if io[1]:
                out_channels = [output.channel - 1 for output in io[1]]
                asio_out = sd.AsioSettings(channel_selectors=out_channels)

                if not io[0]:
                    sd.default.extra_settings = asio_out
                    sd.default.channels = len(out_channels)
                    return
            
            if io[0] and io[1]:
                sd.default.extra_settings = (asio_in, asio_out)
                sd.default.channels = (len(in_channels), len(out_channels))
                return
            
        elif "CoreAudio" in self.device: 
            raise NotImplementedError
            inChannels = [c - 1 for c in channels[0]] # convert to channel names starting with 0
            ca_in = sd.CoreAudioSettings(channel_map=inChannels)

            if channels[1]:
                outChannels = [-1]*sd.query_devices(device=self.device, kind="output")["max_output_channels"]
                for idx, c in enumerate(channels[1]):
                    outChannels[c-1] = idx
                ca_out = sd.CoreAudioSettings(channel_map=outChannels)

                sd.default.extra_settings = (ca_in, ca_out)
                sd.default.channels = (len(inChannels), len(outChannels))
            else:
                sd.default.extra_settings = ca_in
                sd.default.channels = len(inChannels)
        else:
            raise NotImplementedError
        
    def callback(self, indata: np.ndarray, outdata: np.ndarray, frames: int, time):
        """Sounddevice callback function that has to be implemented by the user.
            This function is used for realtime processing auf audio signals in the form of numpy arrays.

        Args:
            indata (np.ndarray): Data optained by the interface (blocksize x channels)
            outdata (np.ndarray): Data written to the interface (blocksize x channels)
            frames (int): blocksize
            time (_type_): CDate time object to process ADC/DAC timings (used to compute latency).

        Raises:
            NotImplementedError: No callback implemnented by user
        """
        raise NotImplementedError("No callback implemnented by user")
                
    def _callback(self, indata: np.ndarray, outdata: np.ndarray, frames: int, time, status) -> None:
        if status:
            print(status, flush=True)

        outdata.fill(0)
        self.callback(indata, outdata, frames, time)

    def stream(self, io:Tuple[List[Input], List[Output]], finished_callback: Callable=None) -> sd.Stream:
        """Initiializes sounddevice with the classes attributes for the given lists of inputs and outputs, then returns the sounddevice.Stream to be used in a with statement tos tart the stream.

        !!! warning
            Streams are currently only working for ASIO devices (Windows).

        Args:
            io (tuple of lists): Tuple that contains lists of Input and Output objects.
                If one of them is not needed, leave list empty.
            finished_callback (Callable, optional): User-supplied function which will be called when the stream becomes inactive

        Returns:
            sd.Stream: Stream class to be used in a with statement.

        Raises:
            AttributeError: No audio device specified

        Example:
            ```python linenums="1"
            from asmu import ASetup

            setup = ASetup(setup_path)
            with setup.interface.stream((setup.inputs, setup.outputs)) as stream:
            
                # Start refill and processing threads

                input("Press ENTER to stop stream!")
                stream.stop()
            ```
        """
        try:
            self._init_sounddevice(io)
        except AttributeError as exc:
            raise exc
        return sd.Stream(callback=self._callback, finished_callback=finished_callback)
    
    def stop_stream(self, exc_type, exc_value, traceback) -> None:
        """Stops the interface stream.

        Raises:
            sd.CallbackStop: Stop the sounddevice Stream.
        """
        raise sd.CallbackStop

    


    

       