from contextlib import suppress as _suppress

from django.core.exceptions import FieldDoesNotExist as _FieldDoesNotExist
from django.db import models as _models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError as _ValidationError
from rest_framework.permissions import SAFE_METHODS as _SAFE_METHODS

from b2_utils.serializers.relations import DynamicFieldsSerializer

___all__ = [
    "DynamicListMixin",
    "UserQuerysetMixin",
]


class DynamicListMixin:
    """
    Allow client to specify which fields to return in the response, and optimize the query
    using select and prefetch related.
    This Function only performs on list action.

    Examples:
        # serializer.py
        # Required to use DynamicFieldsSerializer
        class FooSerializer(DynamicFieldsSerializer, serializers.ModelSerializer):
            class Meta:
                model = Foo
                fields = ["id", "name", "email", "phone"]

        #views.py
        class FooViewSet(DynamicListMixin, viewsets.ModelViewSet):
            queryset = Foo.objects.all()
            serializer_class = FooSerializer
    """

    list_fields: list[str] | None
    select_related_fields: list[str] | None
    prefetch_related_fields: list[str] | None

    def _validate_query_fields(self, fields: list[str]):
        if any(field not in self.serializer_class.Meta.fields for field in fields):
            raise _ValidationError(_("Invalid query fields."))

    def get_serializer(self, *args, **kwargs):
        if not issubclass(self.serializer_class, DynamicFieldsSerializer):
            msg = "Serializer class must be a subclass of DynamicFieldsSerializer."
            raise TypeError(msg)

        if (
            hasattr(self, "list_fields")
            and self.action == "list"
            and self.request.method in _SAFE_METHODS
        ):
            return self.serializer_class(
                *args,
                fields=self.list_fields,
                context=self.get_serializer_context(),
                **kwargs,
            )

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if (
            (fields := self.request.query_params.get("fields"))
            and self.action == "list"
            and self.request.method in _SAFE_METHODS
        ):
            self._validate_query_fields(fields.split(","))

            self._set_fields()

            if self.select_related_fields:
                queryset = queryset.select_related(*self.select_related_fields)

            if self.prefetch_related_fields:
                queryset = queryset.prefetch_related(*self.prefetch_related_fields)

            return queryset

        return queryset

    def _set_fields(self):
        self._set_list_fields()
        self._set_related_fields()
        self._set_prefetch_related_fields()

    def _set_list_fields(self):
        if fields := self.request.query_params.get("fields"):
            self.list_fields = fields.split(",")

    def _set_related_fields(self):
        self.select_related_fields = self._get_select_related_fields()

    def _set_prefetch_related_fields(self):
        self.prefetch_related_fields = self._get_prefetch_related_fields()

    def _get_select_related_fields(self):
        with _suppress(_FieldDoesNotExist):
            return [
                field
                for field in self.list_fields
                if isinstance(
                    self.serializer_class.Meta.model._meta.get_field(field),
                    _models.ForeignKey | _models.OneToOneField,
                )
            ]

    def _get_prefetch_related_fields(self):
        with _suppress(_FieldDoesNotExist):
            return [
                field
                for field in self.list_fields
                if isinstance(
                    self.serializer_class.Meta.model._meta.get_field(field),
                    _models.ManyToManyField
                    | _models.ManyToOneRel
                    | _models.ManyToManyRel,
                )
            ]


class UserQuerysetMixin:
    """
    This mixin allow define queryset for each user role, using manager methods.
    The method name must be in the format: get_for_{role_name}
    if method not found, return default queryset.

    Examples:
        class User(models.Model):
            class Roles(models.TextChoices):
                ADMIN = "admin", "Admin"
                MEMBER = "member", "member"
            role = models.CharField(max_length=10, choices=Roles.choices)

        class Foo(models.Model):
            objects = FooManager()

        class FooManger(models.Manager):
            def get_for_admin(self, queryset, request):
                pass # do something

            def get_for_user(self, queryset, request):
                pass # do something
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return self._get_queryset_for_user(queryset)

    def _get_queryset_for_user(self, queryset):
        try:
            return getattr(
                self.serializer_class.Meta.model.objects,
                f"get_for_{self.request.user.role_display}",
            )(
                queryset,
                self.request,
            )

        except AttributeError:
            return queryset
