from rest_framework import status as _status
from rest_framework.response import Response as _Response

__all__ = [
    "InactivateMixin",
]


class InactivateMixin:
    """
    This mixins assumes that the queryset model has an `is_active` field, and
    an method called `inactivate` that sets `activate` to False.

    Ex::

        class Foo(models.Model):
            is_active = models.BooleanField(default=True)

        ### View ##

        class FooViewSet(InactivateMixin, viewsets.ModelViewSet):

            queryset = Foo.objects.all()

            @action(methods=["post"], detail=True)
            def inactivate(self,_,pk=None):
                return super().inactivate()
    """

    def inactivate(self):
        instance = self.get_object()
        instance.inactivate()

        return _Response(status=_status.HTTP_204_NO_CONTENT)

    def activate(self):
        instance = self.get_object()
        instance.activate()

        return _Response(status=_status.HTTP_204_NO_CONTENT)
