from celery import shared_task
from logging import getLogger

from django.conf import settings
from django.core.mail import send_mail

from tasks.models import Task
from tasks.utils import ActionError


logger = getLogger('django')


@shared_task(bind=True)
def notify_client(self, task_id: int):
    try:
        task = Task.objects.select_related('user').get(pk=task_id)
    except Task.DoesNotExist as e:
        raise ActionError(f'task does not found id={task_id}')

    logger.info(f'sending message to email {task.user.email}')
    send_mail(
        'Task execute',
        f'{task.title} is done.',
        settings.EMAIL_HOST_USER,
        [task.user.email],
        fail_silently=False,
    )
    
    return None
