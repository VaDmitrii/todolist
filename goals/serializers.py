from datetime import date

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

from core.models import User
from core.serializers import CoreSerializer
from goals.models import Goal, GoalComment, GoalCategory, Board, BoardParticipant


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices[1:])
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "is_deleted")

    def update(self, instance: Board, validated_data: dict) -> Board:
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

            return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all()
    )

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted",)
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = CoreSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "is_deleted", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user.id != self.context["request"].user.id:
            raise PermissionDenied

        return value

    def validate_due_date(self, value: date) -> date:
        if value and value < timezone.now().date():
            raise ValidationError("Failed to set due date in the past")
        return value


class GoalSerializer(serializers.ModelSerializer):
    user = CoreSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')
        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context['request'].user.id
        ).exists():
            raise PermissionDenied
        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    user = CoreSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
