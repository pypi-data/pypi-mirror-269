"""Scope type definitions."""
from enum import Enum


class MeasurementType(Enum):
    """Measurement types allowed on sensors."""

    TEMPERATURE = "temperature"
    PH = "pH"
    MAGNETIC_FIELD = "magnetic_field"
    ELECTRIC_FIELD = "electric_field"
    CONDUCTIVITY = "conductivity"
    RESISTANCE = "resistance"
    VOLTAGE = "voltage"
    PRESSURE = "pressure"
    FLOW = "flow"
    STRESS = "stress"
    STRAIN = "strain"
    SHEAR = "shear"
    SURFACE_PRESSURE = "surface_pressure"
