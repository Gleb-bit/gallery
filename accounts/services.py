import random
import string

from django.utils import timezone

from accounts.models import User
from gallery_and_user.utils import Util


def generate_code():
    code = ''.join(random.choice(string.digits) for _ in range(4))
    return code


def verify_code(input_code: str, code: str, code_expires: timezone) -> bool:
    if code_expires and code_expires < timezone.now():
        return False
    elif code != input_code:
        return False
    return True


def set_email_verify_code(user, code, code_expires):
    user.temp.email_verify_code = code
    user.temp.email_verify_code_expires = code_expires
    user.temp.save()


def set_or_check_code_and_get_data(validated_data, check_code=False, set_code=False, code=None, code_expires=None):
    return_data = {}

    user = User.objects.get(email=validated_data['email'])

    if check_code:
        is_valid_code = verify_code(
            input_code=validated_data['code'],
            code=user.temp.email_verify_code,
            code_expires=user.temp.email_verify_code_expires
        )
        return_data['is_valid_code'] = is_valid_code

    elif set_code:
        set_email_verify_code(user, code, code_expires)

        email_body = '    Здравствуйте!\n' \
                     'Для смены пароля введите указанный ' \
                     'ниже код в приложении: \n' + str(code)

        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Код подтверждения ' + str(code)}
        Util.send_email(data)

    return_data['user'] = user
    return return_data

