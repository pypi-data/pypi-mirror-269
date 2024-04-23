"""
Conversion Handlers - Textual/Markup

This module provides classes for converting between different markup file formats. It includes concrete implementations of conversion classes for various file types (txt, md, html, ...).
"""

from typing import List

from opencf_core.base_converter import BaseConverter
from opencf_core.filetypes import FileType
from opencf_core.io_handler import StrToTxtWriter, TxtToStrReader


class TextToTextConverter(BaseConverter):
    """
    Converts text files to text format.
    """

    file_reader = TxtToStrReader()
    file_writer = StrToTxtWriter()


class TXTToMDConverter(TextToTextConverter):
    """
    Converts text files to Markdown format.
    """

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.TEXT

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.MARKDOWN

    def _convert(self, input_contents: List[str]):
        md_content = "\n".join(input_contents)
        return md_content
