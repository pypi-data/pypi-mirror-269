import pandas as pd

# TODO - Replace return types with Gable Types
# from gable.openapi import (
#     FieldModel,
#     GableSchemaBool,
#     GableSchemaFloat,
#     GableSchemaInt,
#     GableSchemaList,
#     GableSchemaNull,
#     GableSchemaString,
#     GableSchemaStruct,
#     GableSchemaType,
#     GableSchemaUnion,
# )


class NativeS3Converter:
    def __init__(self):
        pass

    def to_recap(self, df: pd.DataFrame, event_name: str) -> dict:
        """
        Convert a pandas DataFrame to a Recap StructType.
        Args:
            df (pd.DataFrame): The pandas DataFrame to convert.
            event_name (str): The name of the field.
        Returns:
            StructType: The Recap StructType representing the DataFrame.
        """
        schema = self._get_schema(df)
        nullable = df.isnull().any()
        fields = []
        for field_name, field_dtype in schema.items():
            try:
                # Handle column representing nested JSON field
                # ex: customerDetails.technicalContact.email
                if "." in field_name:
                    self._handle_nested_fields(
                        field_name, field_dtype, nullable, fields
                    )
                else:
                    gable_type = self._parse_type(
                        field_dtype, field_name, nullable[field_name]  # type: ignore
                    )
                    fields.append(gable_type)
            except ValueError as e:
                print(f"Error parsing field {field_name} of type {field_dtype}: {e}")

        return {"fields": fields, "name": event_name, "type": "struct"}

    def _parse_type(self, dtype: str, field_name: str, nullable: bool) -> dict:
        """
        Parse a Dataframe dtype and return the corresponding Gable Type.
        Args:
            field_type (str): The field type to parse.
            field_name (str): The name of the field.
            nullable (bool): Whether the field is nullable.
        Returns:
            The Gable Type corresponding to the field type.
        """

        if dtype == "string":
            type = {"type": "string", "name": field_name}
        elif dtype == "Int64":
            type = {"type": "int", "name": field_name}
        elif dtype == "Float64":
            type = {"type": "float", "name": field_name}
        elif dtype == "boolean":
            type = {"type": "bool", "name": field_name}
        elif dtype == "object":
            # TODO - figure out what is inside the list
            type = {"type": "list", "name": field_name}
        else:
            raise ValueError(f"Unsupported dtype: {dtype}")

        if nullable:
            type = {
                "type": "union",
                "types": [type, {"type": "null"}],
                "name": field_name,
            }
            # in conversations with Adrian and Suzanne, we determined that it's safe (in the short term)
            # to assume that when a dtype is an object and also nullable, that it's a null type.
            # the above todo for determining list types will need to be tackled in future work and may include a refactoring to replace pandas for JSON parsing/inference
            if dtype == "object":
                type = {
                    "type": "null",
                    "name": field_name,
                }

        return type

    def _handle_nested_fields(
        self,
        field_name: str,
        field_type: str,
        nullable,
        current_level_fields: list[dict],
    ):
        """
        Handle nested fields in a DataFrame.
        Args:
            field_name (str): The name of the field.
            field_type (str): The field type to parse.
            nullable (pd.Series): Whether the field is nullable.
            current_level_fields (list): The current "level" of fields.
        """

        field_name_parts = field_name.split(".")
        # Iterate through each "level" of the nested fields
        for index, subfield_name in enumerate(field_name_parts):
            # Look to see if the subfield has already been added to the current level
            found_recap_type = next(
                (
                    field
                    for field in current_level_fields
                    if field["name"] == subfield_name
                ),
                None,
            )
            if found_recap_type is not None:
                subfield_recap_type = found_recap_type
            else:
                if index == len(field_name_parts) - 1:
                    # Last item in the list is not a StructType
                    subfield_recap_type = self._parse_type(
                        field_type,
                        subfield_name,
                        nullable[field_name],
                    )
                else:
                    subfield_recap_type = {
                        "fields": [],
                        "name": subfield_name,
                        "type": "struct",
                    }
                current_level_fields.append(subfield_recap_type)

            if subfield_recap_type["type"] == "struct":
                # Update current_level_fields to the next "level"
                current_level_fields = subfield_recap_type["fields"]

    def _get_schema(self, df: pd.DataFrame) -> dict[str, str]:
        # If dataframe is from no header csv and column names are ints, we convert them to strings
        df.columns = df.columns.astype(str)
        return df.convert_dtypes().dtypes.to_dict()
