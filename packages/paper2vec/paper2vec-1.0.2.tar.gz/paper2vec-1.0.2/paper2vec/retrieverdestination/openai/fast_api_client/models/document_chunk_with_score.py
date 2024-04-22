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
  from ..models.document_chunk_metadata import DocumentChunkMetadata





T = TypeVar("T", bound="DocumentChunkWithScore")


@_attrs_define
class DocumentChunkWithScore:
    """ 
        Attributes:
            text (str):
            metadata (DocumentChunkMetadata):
            score (float):
            id (Union[Unset, str]):
            embedding (Union[Unset, List[float]]):
     """

    text: str
    metadata: 'DocumentChunkMetadata'
    score: float
    id: Union[Unset, str] = UNSET
    embedding: Union[Unset, List[float]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.document_chunk_metadata import DocumentChunkMetadata
        text = self.text

        metadata = self.metadata.to_dict()

        score = self.score

        id = self.id

        embedding: Union[Unset, List[float]] = UNSET
        if not isinstance(self.embedding, Unset):
            embedding = self.embedding






        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "text": text,
            "metadata": metadata,
            "score": score,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if embedding is not UNSET:
            field_dict["embedding"] = embedding

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.document_chunk_metadata import DocumentChunkMetadata
        d = src_dict.copy()
        text = d.pop("text")

        metadata = DocumentChunkMetadata.from_dict(d.pop("metadata"))




        score = d.pop("score")

        id = d.pop("id", UNSET)

        embedding = cast(List[float], d.pop("embedding", UNSET))


        document_chunk_with_score = cls(
            text=text,
            metadata=metadata,
            score=score,
            id=id,
            embedding=embedding,
        )

        document_chunk_with_score.additional_properties = d
        return document_chunk_with_score

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
