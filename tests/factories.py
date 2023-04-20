import datetime

import factory.django

from core.models import User
from goals.models import BoardParticipant, Board, GoalCategory, Goal, GoalComment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_user"
    password = "test123"
    email = "tests@test.ru"
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = "test board"
    is_deleted = False


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = 1


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = "test_category"
    user = factory.SubFactory(UserFactory)
    is_deleted = False
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = "test goal"
    category = factory.SubFactory(GoalCategoryFactory)
    description = "test description"
    user = factory.SubFactory(UserFactory)
    priority = 2


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = "test comment"
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
