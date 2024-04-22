from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Dict
from typing import cast, List
from typing import cast

if TYPE_CHECKING:
  from ..models.query_result import QueryResult





T = TypeVar("T", bound="QueryResponse")


@_attrs_define
class QueryResponse:
    """ 
        Attributes:
            results (List['QueryResult']):
     """

    results: List['QueryResult']
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.query_result import QueryResult
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)






        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "results": results,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.query_result import QueryResult
        d = src_dict.copy()
        results = []
        _results = d.pop("results")
        for results_item_data in (_results):
            results_item = QueryResult.from_dict(results_item_data)



            results.append(results_item)


        query_response = cls(
            results=results,
        )

        query_response.additional_properties = d
        return query_response

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
