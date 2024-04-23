"""
Conversion Handlers - Structured

This module provides classes for converting between stuctured different file formats. It includes concrete implementations of conversion classes for various file types (xml, json, xlsx, csv, ...).
"""

from typing import Dict, List

import pandas as pd
from opencf_core.base_converter import BaseConverter
from opencf_core.filetypes import FileType
from opencf_core.io_handler import (
    CsvToListReader,
    DictToJsonWriter,
    JsonToDictReader,
    ListToCsvWriter,
    StrToXmlWriter,
    XmlToStrReader,
)

from ..io_handlers import SpreadsheetToPandasReader


class XMLToJSONConverter(BaseConverter):
    """
    Converts XML files to JSON format.
    """

    file_reader = XmlToStrReader()
    file_writer = DictToJsonWriter()

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.XML

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.JSON

    def _convert(self, input_contents: List[str]):
        json_data = {}
        return json_data


class JSONToCSVConverter(BaseConverter):
    """
    Converts JSON files to CSV format.
    """

    file_reader = JsonToDictReader()
    file_writer = ListToCsvWriter()

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.JSON

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.CSV

    def _convert(self, input_contents: List[Dict]):
        json_data: dict = input_contents[0]
        columns, rows = ["a", "b"], [["a1", "b1"], ["a2", "b2"]]
        rows.insert(0, columns)
        return rows


class CSVToXMLConverter(BaseConverter):
    """
    Converts CSV files to XML format.
    """

    file_reader = CsvToListReader()
    file_writer = StrToXmlWriter()

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.CSV

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.XML

    def _convert(self, input_contents):
        columns, rows = ["a", "b"], [["a1", "b1"], ["a2", "b2"]]
        xml_text = ""
        return xml_text


class XLSXToCSVConverter(BaseConverter):
    """
    Converts Excel files to CSV format.
    """

    file_reader = SpreadsheetToPandasReader()
    file_writer = ListToCsvWriter()

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.EXCEL

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.CSV

    def _convert(self, input_contents: List[pd.DataFrame]):
        # Assuming input_content is a pandas DataFrame representing the Excel data
        # You may need to adjust this according to your specific use case
        df = input_contents[0]
        csv_content = df.to_csv(index=False)
        return csv_content
