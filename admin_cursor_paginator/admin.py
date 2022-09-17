import django

from django.contrib import admin

from .paginator import AdminCursorPaginator
from .views import CursorPaginatorChangeList


class CursorPaginatorAdmin(admin.ModelAdmin):
    # django built-in params
    change_list_template = 'admin_cursor_paginator/change_list.html'
    sortable_by = ()
    show_full_result_count = False
    actions_selection_counter = False

    # specific cursor paginator params
    cursor_ordering_field = '-pk'
    show_query_result_count = True

    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
        # django built-in `history_view` shares `ModelAdmin` paginator,
        # so we need to pass original one for this specific case
        if django.VERSION >= (4, 1):
            from django.contrib.admin.models import LogEntry
            if queryset.model is LogEntry:
                return self.paginator(queryset, per_page, orphans, allow_empty_first_page)

        return AdminCursorPaginator(request, queryset, per_page, self.cursor_ordering_field)

    def get_changelist(self, request, **kwargs):
        return CursorPaginatorChangeList
