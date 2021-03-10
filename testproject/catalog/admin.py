from django.contrib import admin

from admin_cursor_paginator import CursorPaginatorAdmin

from .models import Product


@admin.register(Product)
class ProductAdmin(CursorPaginatorAdmin):
    cursor_ordering_field = '-pk'
    list_display = ['id', 'name', 'created_at_iso']
    list_display_links = ['name']
    list_per_page = 10
    actions = None

    def created_at_iso(self, obj):
        return obj.created_at.isoformat()
