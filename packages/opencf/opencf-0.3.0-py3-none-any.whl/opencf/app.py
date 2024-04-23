"""
Main Module

This module contains the main application logic.
"""

import argparse

from opencf_core.converter_app import BaseConverterApp

from .converters import (
    CSVToXMLConverter,
    ImageToPDFConverter,
    ImageToVideoConverterWithOpenCV,
    ImageToVideoConverterWithPillow,
    JSONToCSVConverter,
    PDFToDocxConvertor,
    PDFToImageExtractor,
    TXTToMDConverter,
    VideoToGIFConverter,
    XLSXToCSVConverter,
    XMLToJSONConverter,
)


class ConverterApp(BaseConverterApp):
    """
    Application for file conversion.
    """

    converters = [
        XMLToJSONConverter,
        JSONToCSVConverter,
        CSVToXMLConverter,
        TXTToMDConverter,
        XLSXToCSVConverter,
        ImageToPDFConverter,
        # PDFToImageConverter,
        PDFToImageExtractor,
        ImageToVideoConverterWithPillow,
        ImageToVideoConverterWithOpenCV,
        VideoToGIFConverter,
        PDFToDocxConvertor,
    ]


def main():
    """
    Main function to run the file conversion application.
    """
    parser = argparse.ArgumentParser(description="File BaseConverter App")
    parser.add_argument("files", nargs="+", type=str, help="Paths to the input files")
    parser.add_argument(
        "-t", "--input-file-type", type=str, help="Type of the input file"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="",
        help="Path to the output file (optional)",
    )
    parser.add_argument(
        "-ot", "--output-file-type", type=str, help="Type of the output file (optional)"
    )
    args = parser.parse_args()

    input_file_paths = args.files
    input_file_type = args.input_file_type
    output_file_path = args.output_file
    output_file_type = args.output_file_type

    app = ConverterApp(
        input_file_paths, input_file_type, output_file_path, output_file_type
    )
    app.run()


if __name__ == "__main__":
    main()
