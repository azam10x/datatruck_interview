from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Book


class BookSerializer:
    def __init__(self, instance=None, data=None, many=False):
        """
        Initialize the serializer with a model instance or input data.
        :param instance: A Book instance or queryset (optional).
        :param data: Input data for validation and deserialization (optional).
        :param many: If True, handle multiple objects (e.g., querysets).
        """
        self.instance = instance
        self.data = data
        self.many = many
        self.errors = []
        self.validated_data = None

    def to_representation(self):
        """
        Convert a model instance (or queryset) to a dictionary 
        (or list of dictionaries).
        """
        if self.many and self.instance:
            return [
                self._to_representation_object(obj) for obj in self.instance
            ]
        elif self.instance:
            return self._to_representation_object(self.instance)
        return {}

    def _to_representation_object(self, obj):
        """
        Helper method to serialize a single object.
        """
        return {
            "title": obj.title,
            "author": obj.author,
            "publication_date": obj.publication_date.isoformat(),
            "available": obj.available,
        }

    def is_valid(self):
        """
        Validate the input data.
        :return: True if data is valid, False otherwise.
        """
        if self.many:
            self.errors = [self._validate_single(d) for d in self.data]
            self.validated_data = [
                d for d, e in zip(self.data, self.errors) if e is None
            ]
            return all(e is None for e in self.errors)
        else:
            self.errors = self._validate_single(self.data)
            self.validated_data = None if self.errors else self.data
            return self.errors is None

    def _validate_single(self, data):
        """
        Validate a single dictionary of data.
        """
        if not isinstance(data, dict):
            return {"error": "Expected a dictionary."}

        required_fields = ["title", "author", "publication_date", "available"]
        errors = {}

        for field in required_fields:
            if field not in data:
                errors[field] = "This field is required."

        if "publication_date" in data:
            try:
                datetime.strptime(data["publication_date"], "%Y-%m-%d")
            except (ValueError, TypeError):
                errors["publication_date"] = "Invalid date format. Use 'YYYY-MM-DD'."

        if "available" in data and not isinstance(data["available"], bool):
            errors["available"] = "Must be a boolean."

        return errors if errors else None

    def save(self):
        """
        Create or update a model instance using validated data.
        """
        if not self.validated_data:
            raise ValidationError("Cannot save without validated data.")

        if self.many:
            return [
                Book.objects.create(**data) for data in self.validated_data
            ]
        else:
            if self.instance:
                for field, value in self.validated_data.items():
                    setattr(self.instance, field, value)
                self.instance.save()
                return self.instance
            else:
                return Book.objects.create(**self.validated_data)
