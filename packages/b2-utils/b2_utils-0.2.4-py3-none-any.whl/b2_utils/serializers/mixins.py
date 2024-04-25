from rest_framework import fields as _fields


class RelatedFieldWithSerializer:
    def __init__(self, representation_serializer, write_protected=False, **kwargs):
        self.representation_serializer = representation_serializer
        self.write_protected = write_protected

        super().__init__(**kwargs)

    def validate_empty_values(self, data):
        if self.write_protected:
            raise _fields.SkipField

        return super().validate_empty_values(data)
