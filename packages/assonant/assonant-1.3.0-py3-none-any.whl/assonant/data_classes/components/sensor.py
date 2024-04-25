"""Assonant Sensor component data class."""

from ..enums import MeasurementType
from .component import Component


class Sensor(Component):
    """Data class to handle all data required to define a sensor with a specific measurement.

    This class was created handle measurements that are not necessarly related to a specific device.
    That saidwhen some measurement is done related to the Sample or to a specific device, the
    information should be store inside the specific class for it and not into a Sensor class.
    """

    measurement_type: MeasurementType
