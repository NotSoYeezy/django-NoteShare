from django.test import TestCase
from notes.validators import check_file_extension
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile


class TestCheckFileExtensionValidator(TestCase):

    def test_validator_gives_exception(self):
        """Testing if validator raises ValidationError exception correctly"""
        file = SimpleUploadedFile('test.xml', b'content')
        with self.assertRaises(ValidationError):
            check_file_extension(file)