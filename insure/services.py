from .documents import ProductDocument
from elasticsearch_dsl.query import MultiMatch


def search_product(query, filtration):
    products = ProductDocument.search()
    if query and query != "":
        products = products.query(
            MultiMatch(
                query=query,
                fields=[
                    "product.name",
                    "product.description",
                    "product.category.name",
                    "product.company.name",
                ],
            )
        )
    if filtration:
        products = products.sort(filtration)
    return products.to_queryset()
