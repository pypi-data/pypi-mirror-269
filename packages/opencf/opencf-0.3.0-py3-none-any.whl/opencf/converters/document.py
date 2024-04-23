"""
Conversion Handlers - Document

This module provides classes for converting between document different file formats. It includes concrete implementations of conversion classes for various file types (pdf, docx, epub, ...).
"""

from pathlib import Path
from typing import List

from opencf_core.base_converter import BaseConverter
from opencf_core.filetypes import FileType
from pdf2docx import Converter as pdf2docx_converter
from PIL import Image as PillowImage
from PyPDF2 import PdfReader, PdfWriter

from ..io_handlers import ImageToPillowReader, PdfToPyPdfReader, PyPdfToPdfWriter


class ImageToPDFConverter(BaseConverter):
    """
    Converts image files to PDF format.
    """

    file_reader = ImageToPillowReader()
    file_writer = None
    folder_as_output = False

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.IMAGE

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.PDF

    def _convert(self, input_contents: List[PillowImage.Image], output_file: Path):
        images = input_contents

        # Create a list of all the input images and convert them to RGB
        images = [img.convert("RGB") for img in images]

        # Save the PDF file
        images[0].save(output_file, save_all=True, append_images=images[1:])


class ImageToPDFConverterWithPyPdf2(BaseConverter):
    """
    Converts image files to PDF format using PyPDF2.
    """

    file_reader = ImageToPillowReader()
    file_writer = PyPdfToPdfWriter()

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.IMAGE

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.PDF

    def _convert(self, input_contents: List[PillowImage.Image]):
        # Create a new PDF document
        pdf_writer = PdfWriter()

        all_pages = input_contents

        for page in all_pages:
            # Add the image as a page to the PDF document
            width, height = page.size
            pdf_page = pdf_writer.add_blank_page(width=width, height=height)
            pdf_page.merge_page(page)

        return pdf_writer


# class ImageToPDFConverterWithImg2pdf(BaseConverter):
#     """
#     Converts image files to PDF format using img2pdf.
#     """

#     file_reader = None
#     file_writer = None

#     @classmethod
#     def _get_supported_input_type(cls) -> FileType:
#         return FileType.IMAGE

#     @classmethod
#     def _get_supported_output_type(cls) -> FileType:
#         return FileType.PDF

#     def _convert(self, input_contents: List[Path], outputfile: Path):
#         filepaths = input_contents
#         # Convert images to PDF using img2pdf
#         with open(output_file, "wb") as f:
#             f.write(img2pdf.convert(filepaths))


class PDFToImageConverter(BaseConverter):
    """
    Converts PDF files to image format.
    Not implemented yet
    """

    file_reader = PdfToPyPdfReader()
    file_writer = None
    folder_as_output = True

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.IMAGE

    def _convert(self, input_contents: List[PdfReader], output_folder: Path):
        # Assuming you want to convert each page to an image
        pass


class PDFToImageExtractor(BaseConverter):
    """
    Converts PDF files to image format.
    """

    file_reader = PdfToPyPdfReader()
    file_writer = None
    folder_as_output = True

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.IMAGE

    def _convert(self, input_contents: List[PdfReader], output_folder: Path):
        """
        - read more [here](https://pypdf2.readthedocs.io/en/3.0.0/user/extract-images.html)
        """
        pdf_file = input_contents[0]

        for page_num, page in enumerate(pdf_file.pages):
            for count, img in enumerate(page.images):
                fpath = output_folder / f"page{page_num+1}-fig{count+1}-{img.name}"
                with open(str(fpath), "wb") as fp:
                    fp.write(img.data)


class PDFToDocxConvertor(BaseConverter):
    """
    Converts PDF files to docx format using [pdf2docx](https://github.com/ArtifexSoftware/pdf2docx) as recommanded [here](https://stackoverflow.com/a/65932031/16668046)
    There s also a cli interface as presented in [their online](https://pdf2docx.readthedocs.io/en/latest/quickstart.cli.html)
    """

    file_reader = None
    file_writer = None
    folder_as_output = False

    @classmethod
    def _get_supported_input_type(cls) -> FileType:
        return FileType.PDF

    @classmethod
    def _get_supported_output_type(cls) -> FileType:
        return FileType.MSWORD

    def _convert(self, input_contents: List[Path], output_file: Path):
        """
        - read more [here](https://pypdf2.readthedocs.io/en/3.0.0/user/extract-images.html)
        """
        pdf_file = input_contents[0]

        cv = pdf2docx_converter(pdf_file)
        cv.convert(output_file, start=0, end=None)
        cv.close()


class PDFToHTML(BaseConverter):
    """
    i could use this [tool](https://linux.die.net/man/1/pdftohtml) to do it
    """
