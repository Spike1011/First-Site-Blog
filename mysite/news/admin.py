from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category, Inspection


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'update_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

    # вывод на выбранную новость
    fields = ('title', 'category', 'content', 'photo',  'is_published','get_photo', 'views', 'created_at', 'update_at')
    readonly_fields = ('get_photo', 'views', 'created_at', 'update_at')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return "-"

    get_photo.short_description="Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'value')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Inspection, InspectionAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
