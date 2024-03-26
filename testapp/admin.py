from django.contrib import admin

from .models import Category, Article, Author, AdvUser, Machine, Spare, Img

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Author)

# admin.site.register(AdvUser)
# admin.site.register(Machine)
# admin.site.register(Spare)
# admin.site.register(Img)