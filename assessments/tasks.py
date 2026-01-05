import logging
from celery import shared_task
from assessments.models import Submission
from assessments.services import GradingService

logger = logging.getLogger(__name__)

@shared_task
def grade_submission_task(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
        logger.info(f"Starting grading for submission {submission_id}")
        GradingService.grade_submission(submission)
        logger.info(f"Successfully graded submission {submission_id}")
        return True
    except Submission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found during grading task.")
        return False
    except Exception as e:
        logger.error(f"Error grading submission {submission_id}: {e}")
        raise e
