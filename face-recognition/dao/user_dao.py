from db.models import User


def get_users():
    users = User.objects.all()
    return users


