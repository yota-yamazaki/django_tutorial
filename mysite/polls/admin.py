from random import choice

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.db.models import F
from .forms import ChoiceAdminForm
from grappelli.forms import GrappelliSortableHiddenMixin

from .models import Question, Choice, Reservation

class ChoiceInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Choice
    extra = 3
    sortable_excludes = ("votes", "question")

class ReservationInline(admin.TabularInline):
    model = Question.reservation_set.through
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["grp-collapse grp-closed"]}),
    ]
    inlines = [ChoiceInline, ReservationInline]

    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date", "question_text"]
    search_fields = ["question_text"]
    change_list_template = "admin/change_list_filter_confirm_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)

        if obj is None:
            return readonly

        if obj.reservation_set.filter(status="完了").exists():
            return ["question_text"]

        return readonly


class ChoiceAdmin(admin.ModelAdmin):
    actions = ['increment_votes']

    raw_id_fields = ('question',)
    # define the related_lookup_fields
    related_lookup_fields = {
        'fk': ['question'],
    }

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
admin.site.register(Reservation)

