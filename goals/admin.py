from django.contrib import admin

from goals.models import Goal, GoalComment, GoalCategory, Board, BoardParticipant


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated", "is_deleted")


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ("board", "user", "role", "created", "updated")


@admin.register(GoalCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", "board",)
    search_fields = ("title",)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", "description", "category", "due_date")
    search_fields = ("title", "description")


@admin.register(GoalComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "created", "updated", "goal")
