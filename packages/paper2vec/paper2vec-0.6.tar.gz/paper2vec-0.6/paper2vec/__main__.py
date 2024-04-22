import asyncio
from itertools import product
from paper2vec.datasource import alias as datasources
from paper2vec.vectorizer import alias as vectorizers
from paper2vec.datadestination import alias as datadestinations
from paper2vec.retrieverdestination import alias as retrieverdestinations
from paper2vec.abc import run_vectorizer, run_retriever
from argparse import ArgumentParser


def func_parser_gen_vectorizer(datasource_constructor, vectorizer_constructor, datadestination_constructor):
    def func_parser(parser):
        args = parser.parse_args()
        datasource = datasource_constructor(args)
        vectorizer = vectorizer_constructor(args)
        datadestination = datadestination_constructor(args)
        asyncio.get_event_loop().run_until_complete(
            run_vectorizer(datasource, vectorizer, datadestination, batch_size=args.batch_size)
        )
    return func_parser


def func_parser_gen_retriever(datasource_constructor, retriever_constructor):
    def func_parser(parser):
        args = parser.parse_args()
        datasource = datasource_constructor(args)
        retriever = retriever_constructor(args)
        asyncio.get_event_loop().run_until_complete(
            run_retriever(datasource, retriever, batch_size=args.batch_size)
        )
    return func_parser


parser = ArgumentParser()
parser.add_argument("--batch-size", type=int, default=64, help=f'Batch size of vectorize.')
subparsers = parser.add_subparsers(help='sub-command help')
for datasource, vectorizer, datadestination in product(datasources.keys(), vectorizers.keys(), datadestinations.keys()):
    subparser = subparsers.add_parser(
        f"{datasource}-{vectorizer}-{datadestination}",
        help=f"{datasource} -text-> {vectorizer} -vector-> {datadestination}"
    )
    datasources[datasource].add_arguments(subparser)
    vectorizers[vectorizer].add_arguments(subparser)
    datadestinations[datadestination].add_arguments(subparser)
    subparser.set_defaults(func=func_parser_gen_vectorizer(
        datasources[datasource],
        vectorizers[vectorizer],
        datadestinations[datadestination]
    ))
for datasource, retrieverdestination in product(datasources.keys(), retrieverdestinations.keys()):
    subparser = subparsers.add_parser(
        f"{datasource}-{retrieverdestination}",
        help=f"{datasource} -text-> {retrieverdestination}"
    )
    datasources[datasource].add_arguments(subparser)
    retrieverdestinations[retrieverdestination].add_arguments(subparser)
    subparser.set_defaults(func=func_parser_gen_retriever(
        datasources[datasource],
        retrieverdestinations[retrieverdestination]
    ))


# --------- Run ---------
args = parser.parse_args()
args.func(parser)
