'''
vision-locator python library
'''

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from .__module__.__module__ import Module
from .__exception__.__exception__ import DetectException, OcrException
from .__detect__.__detect__ import detect, detect_text


__all__ = [
    'Module',
    'DetectException',
    'OcrException',
    'detect',
    'detect_text'
]
