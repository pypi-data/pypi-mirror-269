import abc
from typing import List, Dict, AsyncGenerator, NamedTuple
from argparse import ArgumentParser


class Config(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def add_arguments(parser: ArgumentParser) -> None:
        pass


class Content(NamedTuple):
    id: str
    text: str
    metadata: Dict


class DataSource(Config):
    @abc.abstractmethod
    async def get_contents(self) -> AsyncGenerator[Content, None]:
        yield


class Vectorizer(Config):
    @abc.abstractmethod
    async def vectorize(self, *contents: str) -> List[List[float]]:
        pass


class Point(NamedTuple):
    id: str
    vector: List[float]
    metadata: Dict


class DataDestination(Config):
    @abc.abstractmethod
    async def write_vectors(self, *vectors: Point) -> None:
        pass


class RetrieverDestination(Config):
    @abc.abstractmethod
    async def upsert(self, *contents: Content) -> None:
        pass


async def run_vectorizer(datasource: DataSource, vectorizer: Vectorizer, datadestination: DataDestination, batch_size: int):
    batch: List[Content] = []
    async for content in datasource.get_contents():
        batch.append(content)
        if len(batch) >= batch_size:
            vectors = await vectorizer.vectorize(*[c.text for c in batch])
            points = [
                Point(id=content.id, vector=vector, metadata=content.metadata) for vector, content in zip(vectors, batch)
            ]
            await datadestination.write_vectors(*points)
            batch = []
    if len(batch) > 0:
        vectors = await vectorizer.vectorize(*[c.text for c in batch])
        points = [
            Point(id=content.id, vector=vector, metadata=content.metadata) for vector, content in zip(vectors, batch)
        ]
        await datadestination.write_vectors(*points)


async def run_retriever(datasource: DataSource, retriever: RetrieverDestination, batch_size: int):
    batch: List[Content] = []
    async for content in datasource.get_contents():
        batch.append(content)
        if len(batch) >= batch_size:
            await retriever.upsert(*batch)
            batch = []
    if len(batch) > 0:
        await retriever.upsert(*batch)
