"""Class module to interface with Airtable.
"""
# pylint: disable=logging-too-many-args
import os

from aracnid_logger import Logger
from dateutil.parser import parse
from pyairtable import Api, Table
from pyairtable.formulas import match


# initialize logging
logger = Logger(__name__).get_logger()


class AirtableInterface:
    """Airtable interface class.

    Environment Variables:
        AIRTABLE_API_KEY: Airtable API key.

    Attributes:
        air_api_key: The Airtable API key.
        base_id: The identifier of the Airtable base.

    Exceptions:
        None.
    """
    def __init__(self, base_id):
        """Initializes the interface with the base ID and the table name.

        Args:
            base_id: The identifier of the Airtable base.
        """
        # read environment variables
        self.air_api_key = os.environ.get('AIRTABLE_API_KEY')

        # initialize api
        self.api = Api(self.air_api_key)

        # set the base id for the interface
        self.base_id = base_id

        # retrieve the base
        bases = self.api.bases()
        self.base = None
        for base in bases:
            if base.id == self.base_id:
                self.base = base
                break

    def get_base_name(self) -> str:
        """Returns the name of the Base

        Returns:
            str: Name of the Base.
        """
        return self.base.name

    def get_table(self, table_name):
        """Returns the specified Airtable table.

        Args:
            table_name: The name of the table in the Airtable Base.
        """
        table = Table(self.air_api_key, self.base_id, table_name)

        return table

    @staticmethod
    def get_airtable_value(
        record, field_name, default=None, suppress_warnings=False):
        """Retrieves the value from an Airtable record field.

        Args:
            record: The Airtable record.
            field_name: The name of the record's field.
            default: The default value of the field.
            suppress_warnings: Flag to turn off warnings.
        """
        field_val = default
        if record:
            if field_name in record:
                field_val = record[field_name]

            elif field_name in record['fields']:
                field_val = record['fields'][field_name]

            if isinstance(field_val, list):
                if len(field_val) == 1:
                    field_val = field_val[0]
                else:
                    if not suppress_warnings:
                        logger.warning(
                            '%s has multiple values: %s', field_name, field_val
                        )

        return field_val

    @staticmethod
    def get_airtable_list(record, field_name, default=None):
        """Retrieves a list from an Airtable record field.

        Args:
            record: The Airtable record.
            field_name: The name of the record's field.
            default: The default value of the field.
        """
        field_val = default
        if field_name in record['fields']:
            field_val = record['fields'][field_name]

        return field_val

    @classmethod
    def get_airtable_datetime(
        cls, record, field_name, default=None, suppress_warnings=False):
        """Retrieves a datetime value from an Airtable record field.

        The datetime value is localized.

        Args:
            record: The Airtable record.
            field_name: The name of the record's field.
            default: The default value of the field.
            suppress_warnings: Flag to turn off warnings.
        """
        field_val = cls.get_airtable_value(
            record, field_name, default, suppress_warnings)

        if field_val:
            dt_local = parse(field_val).astimezone()
            return dt_local

        return None

    @classmethod
    def get_airtable_date(
        cls, record, field_name, default=None, suppress_warnings=False):
        """Retrieves a date value from an Airtable record field.

        Args:
            record: The Airtable record.
            field_name: The name of the record's field.
            default: The default value of the field.
            suppress_warnings: Flag to turn off warnings.
        """
        field_val = cls.get_airtable_value(
            record, field_name, default, suppress_warnings)

        if field_val:
            dte_local = parse(field_val).date()
            return dte_local

        return None

    @classmethod
    def create_record(cls, table, fields):
        """Creates a record with the specified fields.

        Args:
            table: The Airtable Table object.
            fields: The fields for the created record.
        """
        record = None

        record = table.create(fields)

        return record

    @classmethod
    def match_record(cls, table, field_name, field_value):
        """Returns a record that matches the specified field name and value.

        Args:
            table: The Airtable Table object.
            field_name: The name of the record's field.
            field_value: The value of the field.
        """
        record = None

        field_value_escaped = field_value.replace("'", r"\'")
        record = table.first(formula=match({field_name: field_value_escaped}))

        return record

    @classmethod
    def update_record(cls, table, record_id, fields):
        """Updates a record with the specified fields.

        Args:
            table: The Airtable Table object.
            record_id: The Airtable record identifier.
            fields: The fields for the created record.
        """
        record = None

        record = table.update(record_id, fields, typecast=True)

        return record

    @classmethod
    def delete_record(cls, table, record_id):
        """Deletes the specified record.

        Args:
            table: The Airtable Table object.
            record_id: The Airtable record identifier.
        """
        record = None

        record = table.delete(record_id)

        return record
