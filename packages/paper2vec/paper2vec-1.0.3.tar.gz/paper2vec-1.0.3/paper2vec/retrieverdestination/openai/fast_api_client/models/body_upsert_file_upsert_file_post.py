from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json

from ..types import UNSET, Unset

from typing import Union
from ..types import File, FileJsonType
from ..types import UNSET, Unset
from io import BytesIO






T = TypeVar("T", bound="BodyUpsertFileUpsertFilePost")


@_attrs_define
class BodyUpsertFileUpsertFilePost:
    """ 
        Attributes:
            file (File):
            metadata (Union[Unset, str]):
     """

    file: File
    metadata: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_tuple()


        metadata = self.metadata


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file": file,
        })
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict


    def to_multipart(self) -> Dict[str, Any]:
        file = self.file.to_tuple()


        metadata = self.metadata if isinstance(self.metadata, Unset) else (None, str(self.metadata).encode(), "text/plain")


        field_dict: Dict[str, Any] = {}
        field_dict.update({
            key: (None, str(value).encode(), "text/plain")
            for key, value in self.additional_properties.items()
        })
        field_dict.update({
            "file": file,
        })
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict


    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(
             payload = BytesIO(d.pop("file"))
        )




        metadata = d.pop("metadata", UNSET)

        body_upsert_file_upsert_file_post = cls(
            file=file,
            metadata=metadata,
        )

        body_upsert_file_upsert_file_post.additional_properties = d
        return body_upsert_file_upsert_file_post

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
