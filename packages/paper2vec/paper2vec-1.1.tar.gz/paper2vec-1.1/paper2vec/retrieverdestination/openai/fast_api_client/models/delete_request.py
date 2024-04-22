from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Dict
from typing import cast
from ..types import UNSET, Unset
from typing import cast, List
from typing import Union

if TYPE_CHECKING:
  from ..models.document_metadata_filter import DocumentMetadataFilter





T = TypeVar("T", bound="DeleteRequest")


@_attrs_define
class DeleteRequest:
    """ 
        Attributes:
            ids (Union[Unset, List[str]]):
            filter_ (Union[Unset, DocumentMetadataFilter]):
            delete_all (Union[Unset, bool]):  Default: False.
     """

    ids: Union[Unset, List[str]] = UNSET
    filter_: Union[Unset, 'DocumentMetadataFilter'] = UNSET
    delete_all: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.document_metadata_filter import DocumentMetadataFilter
        ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ids, Unset):
            ids = self.ids





        filter_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        delete_all = self.delete_all


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if ids is not UNSET:
            field_dict["ids"] = ids
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if delete_all is not UNSET:
            field_dict["delete_all"] = delete_all

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_metadata_filter import DocumentMetadataFilter
        d = src_dict.copy()
        ids = cast(List[str], d.pop("ids", UNSET))


        _filter_ = d.pop("filter", UNSET)
        filter_: Union[Unset, DocumentMetadataFilter]
        if isinstance(_filter_,  Unset):
            filter_ = UNSET
        else:
            filter_ = DocumentMetadataFilter.from_dict(_filter_)




        delete_all = d.pop("delete_all", UNSET)

        delete_request = cls(
            ids=ids,
            filter_=filter_,
            delete_all=delete_all,
        )

        delete_request.additional_properties = d
        return delete_request

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
