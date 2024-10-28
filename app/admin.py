from django.contrib import admin
from app.models import Project, Category, Donate

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    pass