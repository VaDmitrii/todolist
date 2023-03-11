from django.db import transaction
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import Goal, GoalComment, GoalCategory, Board, BoardParticipant
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, \
    GoalCommentPermissions
from goals.serializers import GoalCategorySerializer, GoalSerializer, GoalCreateSerializer, \
    GoalCommentSerializer, GoalCommentCreateSerializer, \
    GoalCategoryCreateSerializer, BoardSerializer, BoardListSerializer, BoardCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        query = GoalCategory.objects.filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )
        return query


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalListView(ListAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.filter(
            category__board__participants__user_id=self.request.user.id,
            category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self) -> QuerySet[Goal]:
        return (
            Goal.objects.filter(
                category__board__participants__user_id=self.request.user.id,
                category__is_deleted=False
            ).exclude(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        instance.is_deleted = True
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentListView(ListAPIView):
    permission_classes = [GoalCommentPermissions]
    serializer_class = GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user_id=self.request.user.id
        ).exclude(
            goal__status=Goal.Status.archived
        )


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [GoalCommentPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(
            user=self.request.user
        ).exclude(
            goal__status=Goal.Status.archived
        )


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)


class BoardListView(ListAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    filter_backends = [filters.OrderingFilter]
    pagination_class = LimitOffsetPagination
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )
