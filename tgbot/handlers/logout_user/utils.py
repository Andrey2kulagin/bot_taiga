from users.models import User


def delete_user(tg_id):
    user = User.objects.get(user_id=tg_id)
    user.delete()
