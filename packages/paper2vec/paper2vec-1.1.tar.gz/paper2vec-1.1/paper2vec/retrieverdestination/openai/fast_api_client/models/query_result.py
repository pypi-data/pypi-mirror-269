from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Dict
from typing import cast, List
from typing import cast

if TYPE_CHECKING:
  from ..models.document_chunk_with_score import DocumentChunkWithScore





T = TypeVar("T", bound="QueryResult")


@_attrs_define
class QueryResult:
    """ 
        Attributes:
            query (str):
            results (List['DocumentChunkWithScore']):
     """

    query: str
    results: List['DocumentChunkWithScore']
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.document_chunk_with_score import DocumentChunkWithScore
        query = self.query

        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()
            results.append(results_item)






        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "query": query,
            "results": results,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_chunk_with_score import DocumentChunkWithScore
        d = src_dict.copy()
        query = d.pop("query")

        results = []
        _results = d.pop("results")
        for results_item_data in (_results):
            results_item = DocumentChunkWithScore.from_dict(results_item_data)



            results.append(results_item)


        query_result = cls(
            query=query,
            results=results,
        )

        query_result.additional_properties = d
        return query_result

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
