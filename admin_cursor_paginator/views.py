from django.contrib.admin.views.main import ChangeList


class CursorPaginatorChangeList(ChangeList):
    def get_ordering(self, *args, **kwargs):
        return [self.model_admin.cursor_ordering_field]

    def get_results(self, *args, **kwargs):
        super().get_results(*args, **kwargs)
        if self.query and self.model_admin.show_query_result_count:
            self.result_count = self.queryset.count()
        else:
            # small hack to prevent full count (which is unknown) from being shown in `search_form.html`
            self.full_result_count = self.result_count
