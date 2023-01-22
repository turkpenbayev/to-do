from logging import getLogger

from rest_framework.authtoken.models import Token
from django.db.models import Q

from tasks.utils import ActionError
from tasks.models import Task, User
from tasks.tasks import notify_client


logger = getLogger('django')


class AuthLogin:

    def __call__(self, username: str, password: str) -> str:
        try:
            user = User.objects.get(
                Q(phone__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return token.key
            else:
                raise ActionError('username or password not correct')
        except User.DoesNotExist:
            raise ActionError('username or password not correct')


class AuthLogout:

    def __call__(self, user: User) -> None:
        Token.objects.filter(user=user).delete()
        return None


class AuthChangePassword:

    def __call__(self, user: User, old_password: str, new_password: str) -> None:
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return None
        else:
            raise ActionError('password not correct')


class ExecuteTask:

    def __call__(self, task_id: int) -> None:
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ActionError('Task does not exist')

        task.is_done = True
        task.save()
        notify_client.apply_async(args=(task_id,))
