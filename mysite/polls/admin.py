from random import choice

from django.contrib import admin
from mysite.admin import polls_admin_site
from django.contrib import messages
from django.utils.translation import ngettext
from django.db.models import F
from .forms import ChoiceAdminForm, QuestionAdminForm
from grappelli.forms import GrappelliSortableHiddenMixin

from .models import Question, Choice, Reservation

class ChoiceInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Choice
    extra = 0
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

    list_display = ["question_text", "pub_date", "was_published_recently", "choice_list"]
    list_filter = ["pub_date", "question_text"]
    search_fields = ["question_text"]
    change_list_template = "admin/change_list_filter_confirm_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"
    form = QuestionAdminForm
    date_hierarchy = "pub_date"

    def choice_list(self, obj):
        items = []
        if obj.choice_set is not None:
            for c in obj.choice_set.all():
                items.append(c.choice_text)
        return items

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))

        if obj is None:
            return readonly

        if obj.reservation_set.filter(status__in=["予約", "チェックイン"]).exists():
            readonly.append("question_text")
            return readonly

        return readonly

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("choice_set")

class ChoiceAdmin(admin.ModelAdmin):
    actions = ['increment_votes', 'decrement_votes']
    list_display =['choice_text', 'votes']

    raw_id_fields = ('question',)
    # define the related_lookup_fields
    related_lookup_fields = {'fk': ['question'],}
    form = ChoiceAdminForm

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

    @admin.action(description="投票数を1減らします")
    def decrement_votes(self, request, queryset):
        updated = queryset.update(votes = F('votes')-1)

        self.message_user(
            request,
            ngettext(
                "%d question votes successfully decrement.",
                "%d questions votes successfully decrement.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


class ReservationAdmin(admin.ModelAdmin):
    list_display = ["reservation_number", "status"]
    filter_horizontal = ("questions",)

polls_admin_site.register(Question, QuestionAdmin)
polls_admin_site.register(Choice, ChoiceAdmin)
polls_admin_site.register(Reservation, ReservationAdmin)

