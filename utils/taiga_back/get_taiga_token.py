from users.models import User


def get_taiga_token_by_tg_id(tg_id):
    user = User.objects.get(user_id=tg_id)
    if user.auth_type == "Bearer":
        return user.auth_token
    else:
        return user.application_token
