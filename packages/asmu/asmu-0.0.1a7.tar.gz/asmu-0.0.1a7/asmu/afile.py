import soundfile
import tempfile
import shutil
import os
import json
from datetime import datetime
import numpy as np


class AFile(soundfile.SoundFile):
    def __init__(self, afile_path:str, mode:str="r", samplerate:int=None, channels:int=None) -> None:
        """The AFile class handles .wav sound files. Metadata is used to store and load additional settings.
        It is recommended to open AFile's in a with statement.

        Args:
            afile_path (str): Path to .wav file.
            mode ({"r", "r+", "w", "w+"}, optional): File open mode.
            samplerate (int, optional): Samplerate, only used in write mode.
            channels (int, optional): Channel count, only used in write mode.

        Example:
            ```python linenums="1" title="Load a file"
            from asmu import AFile

            with AFile(AFILE_PATH) as afile:
                print(afile.data.shape)
            ```
        """
        self._afile_path = afile_path
        if mode == "r":
            super().__init__(afile_path)
        else:
            _name = os.path.split(afile_path)[1].replace(".wav", "")
            self._tmp = tempfile.NamedTemporaryFile(prefix=_name, suffix='.wav', dir="", delete=True)
            super().__init__(self._tmp, mode=mode, samplerate=samplerate, channels=channels, subtype="PCM_24", format="WAV")
            now = datetime.now()
            # set wav metadata
            self.title = _name
            self.date = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # store settings as json string in metadata "comment"
    @property
    def settings(self) -> dict:
        """Additional JSON settings in the metadata's comment field."""
        if not self.comment:
            return {}
        else:
            return json.loads(self.comment)
    @settings.setter
    def settings(self, value: dict) -> None:
        self.comment = json.dumps(value)

    @property
    def latency(self) -> int:
        """Latency in samples."""
        try:
            return int(self.settings["latency"])
        except KeyError:
            return None
    @latency.setter
    def latency(self, value: int) -> None:
        settings = self.settings
        settings["latency"] = int(value)
        self.settings = settings

    @property
    def data(self) -> np.ndarray:
        """Data of AFile as numpy array of shape ("samples" x "channels")."""
        self.flush()
        self.seek(0)
        return self.read(dtype="float32", always_2d=True)
    
    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return object.__getattribute__(self, name)

    def cal_latency(self, time):
        """Calculate and store loopback latency without physical connection.

        !!! warning
            Dont rely on this method, as it only calculates the ADC/DAC's internal latency. 
            Use [latency_from_rec.py](../examples.md/#latency_from_recpy) to compare this result with the real loopback calibration.

        Args:
            time (CData): The time object given in the Interface callback function.
        """
        self.latency = round((time.outputBufferDacTime-time.inputBufferAdcTime)*self.samplerate + 1) # the +1 was measured experimentally (could be the cable?)

    def save_file(self):
        """Persist the temporary file at the given afile_path."""
        self.flush()
        self._tmp.seek(0)
        with open(self._afile_path, 'wb') as file:
            shutil.copyfileobj(self._tmp, file)
