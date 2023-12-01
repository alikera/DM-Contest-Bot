from celery.decorators import task
from celery.utils.log import get_task_logger

from .mails import send_buy_question_mail

logger = get_task_logger(__name__)


@task(name="send_buy_question_mail_task")
def send_buy_question_mail_task(
    email: str, 
    name: str, 
    question_file_path: str, 
    question_title:str):

    logger.info(f"Sent buy question email for team {name}")
    return send_buy_question_mail(email=email, question_file_path=question_file_path, 
                                  question_title=question_title)
