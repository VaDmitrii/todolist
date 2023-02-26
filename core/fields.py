from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import CharField


class PasswordField(CharField):
    """Create field for password"""

    def __init__(self, **kwargs):
        # to show password in closed type in admin
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        # add validators to use django password validators
        self.validators.append(validate_password)
