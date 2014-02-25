__author__ = 'indieman'

from tastypie.resources import ModelResource
from tastypie import fields

from .base import BaseResourceMixin

from blog.models import Category, Post
from api.v1.trip_resource import TagsResource


class BlogCategoryResource(ModelResource, BaseResourceMixin):
    class Meta(BaseResourceMixin.Meta):
        queryset = Category.objects.all()
        allowed_methods = ['get']


class PostResource(ModelResource, BaseResourceMixin):
    category = fields.ToOneField(BlogCategoryResource, attribute='category',
                                 related_name='posts',
                                 full=True, null=True)
    tags = fields.ManyToManyField(TagsResource, attribute='tags',
                                  related_name='posts', full=True, null=True)

    class Meta(BaseResourceMixin.Meta):
        queryset = Post.objects.all()
        allowed_methods = ['get']

        filtering = {
            'created': ('exact', 'range', 'gt', 'gte', 'lt', 'lte'),
            'tags': ('exact', 'range')
        }

        ordering = [
            'created',
        ]
