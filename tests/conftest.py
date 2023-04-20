from pytest_factoryboy import register

from tests.factories import BoardFactory, GoalCategoryFactory, GoalFactory, GoalCommentFactory, UserFactory, \
    BoardParticipantFactory

pytest_plugins = "tests.fixtures"

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(GoalCommentFactory)
