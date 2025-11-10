from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.db.models import F

from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["grp-collapse grp-closed"]}),
    ]
    inlines = [ChoiceInline]

    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class ChoiceAdmin(admin.ModelAdmin):
    actions = ['increment_votes']

    @admin.action(description="投票数を1増やします")
    def increment_votes(self, request, queryset):
        updated = queryset.update(votes = F('votes')+1)

        self.message_user(
            request,
            ngettext(
                "%d question votes successfully increment.",
                "%d questions votes successfully increment.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
