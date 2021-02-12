from django.contrib.admin.views.main import PAGE_VAR
from django.template.defaulttags import register

from ..cursor import encode_cursor


@register.inclusion_tag('admin_cursor_paginator/pagination.html', takes_context=False)
def admin_cursor_pagination(cl):
    page = cl.paginator.current_page
    cur_number = page.number

    first_page_url = ''
    prev_page_url = ''
    next_page_url = ''

    if cur_number > 1:
        first_page_url = cl.get_query_string(remove=[PAGE_VAR])

    if cur_number == 2:
        prev_page_url = first_page_url
    elif page.prev_cursor:
        prev_cursor_repr = encode_cursor(page.prev_cursor)
        prev_page_url = cl.get_query_string(new_params={PAGE_VAR: prev_cursor_repr})

    if page.next_cursor:
        next_cursor_repr = encode_cursor(page.next_cursor)
        next_page_url = cl.get_query_string(new_params={PAGE_VAR: next_cursor_repr})

    return {
        'cl': cl,
        'cur_number': cur_number,
        'first_page_url': first_page_url,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }
