"""Assonant Entry data class."""
from typing import Dict, List, Optional, Type, Union

import numpy as np

from .assonant_data_class import AssonantDataClass
from .components import Beamline
from .data_handlers import DataField, DataHandler, TimeSeries
from .enums import ScopeType
from .exceptions import AssonantDataClassesError


class Entry(AssonantDataClass):
    """Data classes that wraps data into a logical/temporal scope related to the experiment.

    Entries are used to group and represent data in a defined temporal/logical scope of the
    experiment, which is directly define by the field "scope_type". e.g: calibration,
    pre-exposition. Every Entry instance must also have an Beamline object to identify
    with at least the beamline name it is related to.
    """

    scope_type: ScopeType
    beamline: Beamline
    fields: Optional[Dict[str, DataHandler]] = {}

    def add_field(
        self,
        name: str,
        value: Union[int, float, str, List, Type[np.ndarray], None],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray], None]]] = {},
    ):
        """Add new positional field to component that data was collected as a TimeSeries.

        Args:
            name (str): Field name.
            value (Union[int, float, str, List, Type[np.ndarray], None]): Value related to field
            collected data.
            unit (Optional[str], optional): Measurement unit related to value parameter.
            Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray], None]]], optional): Dict
            containing any aditional metadata related to collected data. Defaults to {}.
        """
        try:
            new_field = DataField(
                value=value,
                unit=unit,
                extra_metadata=extra_metadata,
            )
        except Exception as e:
            raise AssonantDataClassesError(f"Failed to create DataField Data Handler for {self.name} Component.") from e
        if name not in self.fields:
            self.fields[name] = new_field
        else:
            raise AssonantDataClassesError(f"Field name already exists on: {self.name} Component.")

    def add_timeseries_field(
        self,
        name: str,
        value: Union[int, float, str, List, Type[np.ndarray], None],
        timestamps: Union[int, float, str, List, Type[np.ndarray], None],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray], None]]] = {},
        timestamps_unit: Optional[str] = None,
        timestamp_extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray], None]]] = {},
    ):
        """Add new positional field to component that data was collected as a TimeSeries.

        Args:
            name (str): Field name.
            value (Union[int, float, str, List, Type[np.ndarray], None]): Value related to field
            collected data.
            timestamps (Union[int, float, str, List, Type[np.ndarray], None]): Timestamps related to data collected
            from the field.
            unit (Optional[str], optional): Measurement unit related to value parameter.
            Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray],
            None]]], optional): Dictionary
            containing any aditional metadata related to collected data. Defaults to {}.
            timestamps_unit (Optional[str], optional): Measurement unit related to
            timestamp field. Defaults to None.
            timestamp_extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray],
            None]]], optional): Dictionary
            containing extra metadata about timestamps field. Defaults to {}.
        """
        try:
            new_field = TimeSeries(
                value=DataField(
                    value=value,
                    unit=unit,
                    extra_metadata=extra_metadata,
                ),
                timestamps=DataField(
                    value=timestamps,
                    unit=timestamps_unit,
                    extra_metadata=timestamp_extra_metadata,
                ),
            )
        except Exception as e:
            raise AssonantDataClassesError(
                f"Failed to create TimeSeries Data Handler for {self.name} Component."
            ) from e
        if name not in self.fields:
            self.fields[name] = new_field
        else:
            raise AssonantDataClassesError(f"Field name already exists on: {self.name} Component.")
