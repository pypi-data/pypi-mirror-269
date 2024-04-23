"""
PDF File I/O Handlers

This module provides classes for reading and writing PDF files using the PyPDF2 library. It includes abstract base classes
and concrete implementations for converting between PDF files and PyPDF2 PdfReader objects.
"""

from pathlib import Path

from opencf_core.io_handler import FileReader, FileWriter
from PyPDF2 import PdfReader, PdfWriter


class PdfToPyPdfReader(FileReader):
    """
    Reads a PDF file and returns a [PyPDF2 PdfReader object](https://pypdf2.readthedocs.io/en/3.0.0/modules/PdfReader.html).
    """

    input_format = PdfReader

    def _check_input_format(self, content: PdfReader) -> bool:
        """
        Validates if the provided content is a PyPDF2 PdfReader object.

        Args:
            content (PdfReader): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF2 PdfReader object, False otherwise.
        """
        return isinstance(content, PdfReader)

    def _read_content(self, input_path: Path) -> PdfReader:
        """
        Reads and returns the content from the given input path as a PyPDF2 PdfReader object.

        Args:
            input_path (Path): The path to the input PDF file.

        Returns:
            PdfReader: The PyPDF2 PdfReader object read from the input file.
        """
        pdf_reader = PdfReader(input_path)
        return pdf_reader


class PyPdfToPdfWriter(FileWriter):
    """
    Writes the provided [PyPDF2 PdfWriter object](https://pypdf2.readthedocs.io/en/3.0.0/modules/PdfWriter.html)
    """

    output_format = PdfWriter

    def _check_output_format(self, content: PdfWriter) -> bool:
        """
        Validates if the provided content is a PyPDF2 PdfWriter object.

        Args:
            content (PdfWriter): The content to be validated.

        Returns:
            bool: True if the content is a PyPDF2 PdfWriter object, False otherwise.
        """
        return isinstance(content, PdfWriter)

    def _write_content(self, output_path: Path, output_content: PdfWriter):
        """
        Writes the provided PyPDF2 PdfWriter object to the given output path as a PDF file.

        Args:
            output_path (Path): The path to the output PDF file.
            output_content (PdfWriter): The PyPDF2 PdfWriter object to be written to the output file.
        """
        with open(output_path, "wb") as output_pdf:
            output_content.write(output_pdf)
