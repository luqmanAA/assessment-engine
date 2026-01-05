from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from assessments.models import QuestionOption, Question, Exam, Submission, StudentAnswer


class QuestionOptionSerializer(ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('id', 'text')


class QuestionSerializer(ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id',
            'text',
            'question_type',
            'options'
        )


class ExamSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = (
            'id',
            'title',
            'description',
            'duration',
            'course',
            'metadata',
            'questions'
        )


class StudentAnswerSerializer(ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = (
            'question',
            'selected_option',
            'short_answer_text'
        )

    def validate(self, data):
        question = data.get('question')
        selected_option = data.get('selected_option')
        short_answer_text = data.get('short_answer_text')

        if question.question_type == 'MCQ':
            if not selected_option:
                raise ValidationError("MCQ questions require a selected option.")
            if selected_option.question != question:
                raise ValidationError("Selected option does not belong to the specified question.")

        elif question.question_type == 'SHORT':
            if not short_answer_text:
                raise ValidationError("Short answer questions require text.")

        return data


class SubmissionSerializer(ModelSerializer):
    answers = StudentAnswerSerializer(many=True)

    class Meta:
        model = Submission
        fields = (
            'id',
            'exam',
            'grade',
            'submitted_at',
            'answers'
        )
        read_only_fields = (
            'grade',
            'submitted_at',
            'student'
        )

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')

        submission = Submission.objects.create(**validated_data)

        for answer_data in answers_data:
            StudentAnswer.objects.create(submission=submission, **answer_data)

        return submission
