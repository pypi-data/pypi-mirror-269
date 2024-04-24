"""Welcome to the API of the asmu module.
From the main [asmu][] module the classes for associated files can be imported.

Other classes and fuctions are grouped into the submodules:

- [asmu.io][]: For audio interface communication and definition of inputs and outputs.
- [asmu.generator][]: Signal chain objects creating or transmitting a signal.
- [asmu.analyzer][]: Signal chain objects consuming or recieving a signal.
"""

from asmu.afile import AFile
from asmu.asetup import ASetup

__all__ = ["AFile", "ASetup", "generator", "analyzer", "io"]
