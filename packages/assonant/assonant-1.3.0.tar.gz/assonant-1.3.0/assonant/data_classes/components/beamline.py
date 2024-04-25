"""Assonant Beamline component data class."""

from ..enums.beamline_name import BeamlineName
from .component import Component


class Beamline(Component):
    """Data class to handle all metadata related to them beamline."""

    name: BeamlineName
