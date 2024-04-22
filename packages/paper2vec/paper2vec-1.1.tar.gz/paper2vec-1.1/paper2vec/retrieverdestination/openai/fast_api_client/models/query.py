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
  from ..models.document_metadata_filter import DocumentMetadataFilter





T = TypeVar("T", bound="Query")


@_attrs_define
class Query:
    """ 
        Attributes:
            query (str):
            filter_ (Union[Unset, DocumentMetadataFilter]):
            top_k (Union[Unset, int]):  Default: 3.
     """

    query: str
    filter_: Union[Unset, 'DocumentMetadataFilter'] = UNSET
    top_k: Union[Unset, int] = 3
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.document_metadata_filter import DocumentMetadataFilter
        query = self.query

        filter_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        top_k = self.top_k


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "query": query,
        })
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if top_k is not UNSET:
            field_dict["top_k"] = top_k

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_metadata_filter import DocumentMetadataFilter
        d = src_dict.copy()
        query = d.pop("query")

        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, DocumentMetadataFilter]
        if isinstance(_filter_,  Unset):
            filter_ = UNSET
        else:
            filter_ = DocumentMetadataFilter.from_dict(_filter_)




        top_k = d.pop("top_k", UNSET)

        query = cls(
            query=query,
            filter_=filter_,
            top_k=top_k,
        )

        query.additional_properties = d
        return query

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
