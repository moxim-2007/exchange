from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Product, Category, Company, ProductInfo


@registry.register_document
class ProductDocument(Document):
    duration = fields.IntegerField()
    price = fields.IntegerField()
    product = fields.ObjectField(
        properties={
            "name": fields.TextField(fielddata=True),
            "description": fields.TextField(fielddata=True),
            "category": fields.ObjectField(properties={"name": fields.TextField(fielddata=True)}),
            "company": fields.ObjectField(properties={"name": fields.TextField(fielddata=True)}),
        }
    )

    class Index:
        name = "product"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = ProductInfo
        related_models = [
            Company,
            Category,
            Product,
        ]

    def get_queryset(self):
        """Return the queryset that should be indexed by this document"""
        return super(ProductDocument, self).get_queryset().select_related("product")

    def get_instances_from_related(self, related_instance):
        """Retrieve the Service instance(s) from the related models"""
        return related_instance.productinfo_set.all()
