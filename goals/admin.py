from django.contrib import admin

from goals.models import Goal, GoalComment, GoalCategory


@admin.register(GoalCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title",)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", "description", "category", "due_date")
    search_fields = ("title", "description")


@admin.register(GoalComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "created", "updated", "goal")
