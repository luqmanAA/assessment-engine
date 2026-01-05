from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from assessments.models import Exam, Submission
from assessments.serializers import ExamSerializer, SubmissionSerializer
from assessments.services import GradingFactory
from helpers.permissions import IsOwnerOnly


# Create your views here.

class ExamViewSet(ReadOnlyModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


class SubmissionViewSet(ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = (IsOwnerOnly, )
    http_method_names = ('get', 'post', 'head', 'options',)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "id",
                type=int,
                location=OpenApiParameter.PATH
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = self.perform_create(serializer)

        self._grade_submission(submission)

        headers = self.get_success_headers(serializer.data)
        return Response(SubmissionSerializer(submission).data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(student=self.request.user)

    def _grade_submission(self, submission: Submission):
        grader = GradingFactory.get_grader()
        total_score = 0.0

        for answer in submission.answers.all():
            question = answer.question
            score = 0.0

            if question.question_type == 'MCQ':
                if answer.selected_option and answer.selected_option.is_correct:
                    score = 1.0
            elif question.question_type == 'SHORT':
                score = grader.grade(question.expected_answer, answer.short_answer_text or "")

            answer.score = score
            answer.save()
            total_score += score

        submission.grade = total_score
        submission.save()