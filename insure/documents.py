from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product, Category, Company, ProductInfo


@registry.register_document
class ProductDocument(Document):
    name = fields.TextField(fielddata=True),
    category = fields.ObjectField(
        properties={
            "name": fields.TextField(fielddata=True),
        }
    )
    company = fields.ObjectField(
        properties={
            "name": fields.TextField(fielddata=True),
        }
    )

    class Index:
        name = "product"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Product
        related_models = [
            ProductInfo,
        ]
