from django.urls import include, path
from rest_framework.routers import DefaultRouter

from assessments.views import ExamViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet)
router.register(r'submissions', SubmissionViewSet, basename='submissions')

urlpatterns = [
    path('', include(router.urls)),
]
