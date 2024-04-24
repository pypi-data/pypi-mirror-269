from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, TypeAlias, Union

ResourceId: TypeAlias = str


class ResourceType(Enum):
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    Spreadsheet = "spreadsheet"
    NetCDF4 = "netcdf4"
    NetCDF3 = "netcdf3"
    GeoTIFF = "geotiff"
    NPDict = "np-dict"
    Shapefile = "shapefile"
    Container = "container"


@dataclass
class CSVProp:
    delimiter: str = ","


# @dataclass
# class SpreadsheetProp:
#     worksheet: Optional[str] = None


@dataclass
class Resource:
    id: ResourceId
    type: ResourceType
    prop: Optional[CSVProp] = None

    @staticmethod
    def deserialize(raw: dict):
        if raw["type"] == ResourceType.CSV.value and raw["prop"] is not None:
            prop = CSVProp(raw["prop"]["delimiter"])
        else:
            prop = None
        return Resource(raw["id"], ResourceType(raw["type"]), prop)

    def is_preprocessing_output(self):
        """Return true if this resource holds output of preprocessing functions"""
        return (
            self.id.startswith(f"__preproc__") and self.type == ResourceType.Container
        )

    @staticmethod
    def create_preprocessing_output(attr_id: str) -> Resource:
        return Resource(
            Resource.get_preprocessing_output_id(attr_id), ResourceType.Container
        )

    @staticmethod
    def get_preprocessing_output_id(attr_id: str) -> str:
        return f"__preproc__{attr_id}"


class ResourceData(ABC):

    @abstractmethod
    def to_dict(self):
        pass


@dataclass
class ResourceDataFile(ResourceData):
    file: str

    def to_dict(self):
        return {"file": self.file}


@dataclass
class ResourceDataString(ResourceData):
    value: Union[str, bytes]

    def to_dict(self):
        return {
            "string": (
                self.value.decode() if isinstance(self.value, bytes) else self.value
            )
        }
