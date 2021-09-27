from django.contrib import admin
from .models import *
# Register your models here.

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']    

admin.site.register(MainCategory, MainCategoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','main_category', 'slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'created_date', 'updated_date', 'display']
    list_editable = ['display']
    list_filter = ['created_date', 'updated_date', 'display']

admin.site.register(Post, PostAdmin)

admin.site.register(Comment)

