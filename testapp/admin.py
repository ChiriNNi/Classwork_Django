from django.contrib import admin

from .models import AdvUser, Machine, Spare, Img, Category, Author, Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'content',
        'created_at'
    )

    search_fields = ('title', 'author')
    list_filter = ('category', 'author')
    readonly_fields = ('created_at',)
    list_display_links = None
    list_editable = ('author', 'category')


admin.site.register(Category)
admin.site.register(Author)
# admin.site.register(AdvUser)
# admin.site.register(Machine)
# admin.site.register(Spare)
# admin.site.register(Img)
