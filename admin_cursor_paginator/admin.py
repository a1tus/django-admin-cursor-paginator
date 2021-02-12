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
        return AdminCursorPaginator(request, queryset, per_page, self.cursor_ordering_field)

    def get_changelist(self, request, **kwargs):
        return CursorPaginatorChangeList
