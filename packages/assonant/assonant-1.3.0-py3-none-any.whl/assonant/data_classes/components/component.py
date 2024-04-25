"""Assonant Component abstract class."""

from typing import Dict, List, Optional, Type, Union

import numpy as np

from ..assonant_data_class import AssonantDataClass
from ..data_handlers import Axis, DataField, DataHandler, TimeSeries
from ..enums import TransformationType
from ..exceptions import AssonantDataClassesError


# TODO: Make this class abstract
class Component(AssonantDataClass):
    """Abstract class that creates the base common requirements to define an Assonant Component.

    Components are more generic definitions which may be composed by many subcomponents if more
    detailing in its composition is desired.
    """

    name: str
    subcomponents: Optional[List["Component"]] = []
    positions: Optional[List[Axis]] = []
    fields: Optional[Dict[str, DataHandler]] = {}

    def add_subcomponent(self, component: Union["Component", List["Component"]]):
        """Add new subcomponent or list of new subcomponents to component.

        Args:
            component (Union[Component, List[Component]]): Component object or List of Components which will be add as
            subcomponent from called Component object.
        """
        if isinstance(component, List):
            for _component in component:
                self.subcomponents.append(_component)
        else:
            self.subcomponents.append(component)

    def add_position(
        self,
        name: str,
        transformation_type: TransformationType,
        value: Union[int, float, str, List, Type[np.ndarray], None],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray], None]]] = {},
    ):
        """Add new positional field to component.

        Args:
            name (str): Axis name.
            transformation_type (TransformationType): Type of transformation done by axis.
            value (Union[int, float, str, List, Type[np.ndarray], None]): Value related to axis
            collected data.
            unit (Optional[str], optional): Measurement unit related to value parameter.
            Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray],
            None]]], optional): Dictionary
            containing any aditional metadata related to collected data. Defaults to {}.
        """
        try:
            new_axis = Axis(
                name=name,
                transformation_type=transformation_type,
                value=DataField(
                    value=value,
                    unit=unit,
                    extra_metadata=extra_metadata,
                ),
            )
        except Exception as e:
            raise AssonantDataClassesError(f"Failed to create Axis Data Handler for {self.name} Component.") from e
        try:
            self.positions.append(new_axis)
        except Exception as e:
            raise AssonantDataClassesError(f"Failed to add Axis to {self.name} Component positions list.") from e

    def add_timeseries_position(
        self,
        name: str,
        transformation_type: TransformationType,
        value: Union[int, float, str, List, Type[np.ndarray], None],
        timestamps: Union[int, float, str, List, Type[np.ndarray], None],
        unit: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray], None]]] = {},
        timestamps_unit: Optional[str] = None,
        timestamp_extra_metadata: Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray], None]]] = {},
    ):
        """Add new positional field to component.

        Args:
            name (str): Axis name
            transformation_type (TransformationType): Transformation type of the Axis
            value (Union[int, float, str, List, Type[np.ndarray], None]): Value related to
            axis collected data
            timestamps (Union[int, float, str, List, Type[np.ndarray], None]): Timestamps
            related to data collected from the axis.
            unit (Optional[str], optional): Measurement unit related to value
            field. Defaults to None.
            extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray],
            None]]], optional): Dictionary
            containing extra metadata about value field. Defaults to {}.
            tracked it as a TimeSeries. Defaults to None.
            timestamps_unit (Optional[str], optional): Measurement unit related to
            timestamp field. Defaults to None.
            timestamp_extra_metadata (Optional[Dict[str, Union[int, float, str, List, Type[np.ndarray],
            None]]], optional): Dict
            containing extra metadata about timestamps field. Defaults to {}.
        """
        # Check if positions should be saved as a DataField or TimeSeries
        try:
            new_axis = Axis(
                name=name,
                transformation_type=transformation_type,
                value=TimeSeries(
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
                ),
            )
        except Exception as e:
            raise AssonantDataClassesError(
                f"Failed to create Axis Data TimeSeries with TimeSeries data for {self.name} Component."
            ) from e
        try:
            self.positions.append(new_axis)
        except Exception as e:
            raise AssonantDataClassesError(
                f"Failed to add Axis with TimeSeries data to {self.name} Component positions list."
            ) from e

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
