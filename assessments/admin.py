from django.contrib import admin
from .models import Exam, Question, QuestionOption, Submission, StudentAnswer


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'short_answer_text', 'score')
    can_delete = False


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration', 'created_at')
    search_fields = ('title', 'course')
    list_filter = ('course', 'is_deleted')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam', 'question_type')
    list_filter = ('exam', 'question_type', 'is_deleted')
    search_fields = ('text',)
    inlines = [QuestionOptionInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'grade', 'is_completed', 'completed_at')
    list_filter = ('exam', 'completed_at', 'is_completed')
    search_fields = ('student__username', 'exam__title')
    readonly_fields = ('completed_at',)
    inlines = [StudentAnswerInline]


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__exam')


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'score')
    readonly_fields = ('submission', 'question', 'selected_option', 'short_answer_text', 'score')