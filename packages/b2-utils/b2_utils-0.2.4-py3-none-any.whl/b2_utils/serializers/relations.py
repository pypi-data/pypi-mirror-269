from rest_framework import relations as _relations

from b2_utils.serializers.mixins import (
    RelatedFieldWithSerializer as _RelatedFieldWithSerializer,
)

__all__ = [
    "PrimaryKeyRelatedFieldWithSerializer",
    "SlugRelatedFieldWithSerializer",
    "DynamicPrimaryKeyRelatedFieldWithSerializer",
    "DynamicFieldsSerializer",
]


class PrimaryKeyRelatedFieldWithSerializer(
    _RelatedFieldWithSerializer,
    _relations.PrimaryKeyRelatedField,
):
    def to_representation(self, value):
        if callable(value):
            return self.representation_serializer(
                value.all(),
                context=self.context,
                many=True,
            ).data

        instance = self.queryset.get(pk=value.pk)

        return self.representation_serializer(instance, context=self.context).data


class SlugRelatedFieldWithSerializer(
    _RelatedFieldWithSerializer,
    _relations.SlugRelatedField,
):
    def to_representation(self, value):
        if callable(value):
            return self.representation_serializer(
                value.all(),
                context=self.context,
                many=True,
            ).data

        instance = self.queryset.get(
            **{self.slug_field: getattr(value, self.slug_field)},
        )

        return self.representation_serializer(instance, context=self.context).data


class DynamicPrimaryKeyRelatedFieldWithSerializer(PrimaryKeyRelatedFieldWithSerializer):
    """
    Work like PrimaryKeyRelatedFieldWithSerializer but allow to specify fields to be serialized
    and the representation_serializer must be have DynamicFieldsSerializer as parent
    """

    def __init__(self, fields=None, **kwargs):
        self.representation_fields = fields

        super().__init__(**kwargs)

    def to_representation(self, value):
        kwargs = {}
        if callable(value):
            kwargs = {
                "instance": value.all(),
                "many": True,
            }
        else:
            kwargs["instance"] = self.queryset.get(pk=value.pk)

        if self.representation_fields:
            kwargs["fields"] = self.representation_fields

        return self.representation_serializer(context=self.context, **kwargs).data


class DynamicFieldsSerializer:
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
