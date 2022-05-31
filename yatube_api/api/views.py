from rest_framework import viewsets, status

from posts.models import Post, Group, Comment

from api.serializers import PostSerializer, GroupSerializer, \
    CommentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        if self.request.user and self.request.auth:
            serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)
        return Response(status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.select_related('post').filter(
            post=self.kwargs.get('post_id')
        )

    def perform_create(self, serializer):
        if self.request.user:
            post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
            serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Попытка изменения чужого комментария'
                f'субъектом {self.request.user}'
            )
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Попытка удаления чужого комментария'
                f'субъектом {self.request.user}')
        instance.delete()
