from rest_framework import serializers

from posts.models import Post, Group, Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(required=False,
                                          slug_field='username',
                                          read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(required=False,
                                          slug_field='username',
                                          read_only=True)
    group = serializers.SlugRelatedField(queryset=Group.objects.all(),
                                         required=False, slug_field='title')

    comments = CommentSerializer(source='post', many=True, required=False)

    class Meta:
        model = Post
        fields = (
            'id', 'text', 'group', 'image', 'pub_date', 'author', 'comments'
        )
