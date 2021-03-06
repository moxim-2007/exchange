from elasticsearch_dsl.query import Q
import redis

from .documents import ProductDocument
from django.conf import settings


def search_product(query, filtration):
    products = ProductDocument.search()[0:10000]
    if query and query != "":
        products = products.query(
            Q(
                "multi_match",
                query=query,
                fields=[
                    "name",
                    "company.name",
                    "category.name",
                ],
                fuzziness="AUTO",
            )
        )
    if filtration:
        products = products.sort(filtration)
    return products.to_queryset()


def add_page_visit(product_id):
    redis_connect = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
    )
    if redis_connect.get(product_id):
        redis_connect.incr(product_id, 1)
    else:
        redis_connect.set(product_id, 1)


def get_count_visit(product_id):
    redis_connect = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
    )
    return redis_connect.get(product_id)
