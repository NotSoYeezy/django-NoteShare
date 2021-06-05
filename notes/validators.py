from django.core.exceptions import ValidationError

import os


def check_file_extension(file):
    extension = os.path.splitext(file.name)[1]
    accepted_extensions = ['.pdf']
    if not extension.lower() in accepted_extensions:
        raise ValidationError('Unsupported file type.')
