import collections.abc
import sys

from django.contrib.admin.views.main import PAGE_VAR
from django.utils.functional import cached_property

from .cursor import Cursor, decode_cursor


class AdminCursorPaginator:
    def __init__(self, request, queryset, per_page, ordering_field):
        self.request = request
        self.queryset = queryset
        self.per_page = int(per_page)
        self.ordering_field = ordering_field
        self.ordering_field_name = ordering_field.lstrip('-')

    def page(self, _):
        return self.current_page

    @cached_property
    def current_page(self):
        encoded_cursor = self.request.GET.get(PAGE_VAR, '')
        cursor = decode_cursor(encoded_cursor)
        cur_number = cursor.number if cursor else 1
        is_reverse = bool(cursor and cursor.is_reverse)

        ordering_field = self.ordering_field
        if is_reverse:
            ordering_field = self._reverse_ordering(ordering_field)

        qs = self.queryset.order_by(ordering_field)
        if cursor:
            qs = self._apply_filter(qs, cursor)

        object_list = list(qs[: self.per_page + 1])
        has_more = len(object_list) > self.per_page
        if has_more:
            object_list = object_list[:-1]
        if is_reverse:
            object_list.reverse()

        prev_cursor = None
        if object_list and cur_number > 2:
            prev_cursor = Cursor(
                value=self._get_value_from_instance(object_list[0]),
                is_reverse=1,
                number=cur_number - 1,
            )

        next_cursor = None
        if object_list and (is_reverse or has_more):
            next_cursor = Cursor(
                value=self._get_value_from_instance(object_list[-1]),
                is_reverse=0,
                number=cur_number + 1,
            )

        return AdminCursorPage(object_list, self, cur_number, prev_cursor, next_cursor)

    @cached_property
    def count(self):
        return sys.maxsize

    def _apply_filter(self, qs, cursor):
        direction = 'gt' if cursor.is_reverse == self.ordering_field.startswith('-') else 'lt'
        lookup = '%s__%s' % (self.ordering_field_name, direction)
        return qs.filter(**{lookup: cursor.value})

    def _get_value_from_instance(self, instance):
        parts = self.ordering_field_name.split('__')
        attr = instance
        while parts:
            attr = getattr(attr, parts[0])
            parts.pop(0)
        return attr

    @classmethod
    def _reverse_ordering(cls, field):
        return field[1:] if field.startswith('-') else ('-' + field)


class AdminCursorPage(collections.abc.Sequence):
    def __init__(self, object_list, paginator, number, prev_cursor, next_cursor):
        self.object_list = object_list
        self.paginator = paginator
        self.number = number
        self.prev_cursor = prev_cursor
        self.next_cursor = next_cursor

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, key):
        return self.object_list.__getitem__(key)

    def __repr__(self):
        return '<Page starting from [%s]>' % (repr(self.object_list[0]) if self.object_list else None)
