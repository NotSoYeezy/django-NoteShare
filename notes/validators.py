from django.core.exceptions import ValidationError

import os


def check_file_extension(file):
    extension = os.path.splitext(file.name)[1]
    accepted_extensions = ['.pdf', '.docx']
    if not extension.lower() in accepted_extensions:
        raise ValidationError('Unsupported file type.')


def check_file_size(file):
    """Checking if file exceeds max weight"""
    if file.size > 2097152:  # 2 MB:
        raise ValidationError('File is too big')
