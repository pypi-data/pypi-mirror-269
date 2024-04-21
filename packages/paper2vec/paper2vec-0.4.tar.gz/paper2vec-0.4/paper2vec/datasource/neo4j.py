from neo4j import AsyncGraphDatabase
from paper2vec.abc import DataSource, Content
from argparse import ArgumentParser


async def get_papers(tx, query):
    papers = []
    for record in await (await tx.run(query)).values():
        if "title" not in record[0]:
            papers.append(None)
            continue
        paper = "Title: " + record[0]["title"]
        payload = {"title": record[0]["title"], "title_hash": record[0]["title_hash"]}
        if "abstract" in record[0]:
            paper += " Abstract: " + record[0]["abstract"]
        content = Content(id=record[0]["title_hash"], text=paper, payload=payload)
        papers.append(content)
    return papers


async def get_total(tx, query):
    records = await (await tx.run(query)).values()
    return records[0][0]


class GraphQuery(DataSource):
    @staticmethod
    def add_arguments(parser: ArgumentParser):
        parser.add_argument("--username", type=str, default=None, help=f'Auth username to neo4j database.')
        parser.add_argument("--password", type=str, default=None, help=f'Auth password to neo4j database.')
        parser.add_argument("--uri", type=str, required=True, help=f'URI to neo4j database.')
        parser.add_argument("--query", type=str,
                            default="MATCH (n:Publication)",
                            help=f'Query to get data. "RETURN n SKIP ... LIMIT <batch_size>" will be added behind.')
        parser.add_argument("--tail", type=int, default=0,
                            help=f'If you only want to get last couple of items, use it.')

    def __init__(self, args):
        self.uri = args.uri
        self.username = args.username
        self.password = args.password
        self.query = args.query
        self.batch_size = args.batch_size
        self.tail = args.tail

    async def get_contents(self):
        async with AsyncGraphDatabase.driver(self.uri, auth=(self.username, self.password)) as driver:
            async with driver.session() as session:
                skip = 0
                if self.tail > 0:
                    total = await session.execute_read(get_total, self.query + " RETURN COUNT(n)")
                    skip = total - self.tail
                papers = await session.execute_read(get_papers, self.query + (" RETURN n SKIP %d LIMIT %d" % (skip, self.batch_size)))
                skip += self.batch_size
                while len(papers) > 0:
                    for paper in papers:
                        if paper is None:
                            continue
                        yield paper
                    papers = await session.execute_read(get_papers, self.query + (" RETURN n SKIP %d LIMIT %d" % (skip, self.batch_size)))
                    skip += self.batch_size
