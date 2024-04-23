"""
Conversion Handlers

This module provides classes for converting between different file formats. It includes concrete implementations of conversion classes for various file types.
"""

from .document import (
    ImageToPDFConverter,
    ImageToPDFConverterWithPyPdf2,
    PDFToDocxConvertor,
    PDFToImageConverter,
    PDFToImageExtractor,
)
from .markup import TXTToMDConverter
from .structured import (
    CSVToXMLConverter,
    JSONToCSVConverter,
    XLSXToCSVConverter,
    XMLToJSONConverter,
)
from .video import (
    ImageToVideoConverterWithOpenCV,
    ImageToVideoConverterWithPillow,
    VideoToGIFConverter,
)
