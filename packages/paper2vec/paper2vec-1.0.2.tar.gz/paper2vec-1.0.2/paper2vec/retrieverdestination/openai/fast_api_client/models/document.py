from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast
from ..types import UNSET, Unset
from typing import Dict

if TYPE_CHECKING:
  from ..models.document_metadata import DocumentMetadata





T = TypeVar("T", bound="Document")


@_attrs_define
class Document:
    """ 
        Attributes:
            text (str):
            id (Union[Unset, str]):
            metadata (Union[Unset, DocumentMetadata]):
     """

    text: str
    id: Union[Unset, str] = UNSET
    metadata: Union[Unset, 'DocumentMetadata'] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.document_metadata import DocumentMetadata
        text = self.text

        id = self.id

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "text": text,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_metadata import DocumentMetadata
        d = src_dict.copy()
        text = d.pop("text")

        id = d.pop("id", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, DocumentMetadata]
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = DocumentMetadata.from_dict(_metadata)




        document = cls(
            text=text,
            id=id,
            metadata=metadata,
        )

        document.additional_properties = d
        return document

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
