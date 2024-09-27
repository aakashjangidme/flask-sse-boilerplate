import logging
from dataclasses import fields, MISSING
from typing import TypeVar, Type, Dict, Any, Callable

from app.exceptions.api_exception import BadRequestException

ModelClass = TypeVar('ModelClass', bound='ValidatorMixin')


class ModelValidatorMixin:
    """
    Mixin for validating model data before instantiation.
    """

    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls: Type[ModelClass], data: Dict[str, Any]) -> None:
        """
        Validate the data before creating a model instance.
        """
        required_fields = {field.name for field in fields(cls) if field.default is MISSING}
        missing_fields = required_fields - data.keys()
        if missing_fields:
            raise BadRequestException(f"Missing required fields: {', '.join(missing_fields)}")

    def run_validations(self) -> None:
        """
        Automatically run validation methods defined for fields.
        Collect validation rules defined in field metadata and log relevant information.
        """

        if not getattr(self, '_validate', False):
            # Skip validation if the dataclass is not marked for validation
            # self.logger.debug(f"Skipping validations for {self.__class__.__name__}. Validation not enabled.")
            return

        errors = []

        self.logger.debug(f"Running validations on instance of {self.__class__.__name__}")

        for field in fields(self):
            value = getattr(self, field.name)
            if 'validators' in field.metadata:
                self.logger.debug(
                    f"Validating field '{field.name}' with value '{value}' using validators: {field.metadata['validators']}")
                for validator in field.metadata['validators']:
                    try:
                        validator(self, field.name, value)
                        self.logger.debug(f"Validation passed for field '{field.name}' with value '{value}'")
                    except ValueError as e:
                        error_message = str(e)
                        error_detail = {
                            "field": field.name,
                            "error": error_message
                        }
                        self.logger.error(error_detail)
                        errors.append(error_detail)

        if errors:
            self.logger.error(f"Validation errors found in {self.__class__.__name__}: {errors}")
            raise BadRequestException(
                message="Validation errors occurred.",
                details=errors
            )


# Utility function for declaring common validators
def required_validator(instance: Any, field_name: str, value: Any):
    if value is None or len(value) < 1:
        raise ValueError(f"Field '{field_name}' is required and cannot be None or empty.")


def min_length_validator(min_length: int) -> Callable[[Any, str, Any], None]:
    def validate(instance: Any, field_name: str, value: Any):
        if value is not None and len(value) < min_length:
            raise ValueError(f"Field '{field_name}' must have at least {min_length} characters.")

    return validate
