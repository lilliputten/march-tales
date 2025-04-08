from import_export import resources

from .models import Author, Rubric, Tag, Track, User


class TrackResource(resources.ModelResource):
    class Meta:
        model = Track
        # import_id_field = 'id'
        # import_id_fields = ('id',)
        # fields = ('id', 'name', 'price',)
        # skip_unchanged = True
        # report_skipped = True
        # dry_run = True


class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author


class RubricResource(resources.ModelResource):
    class Meta:
        model = Rubric


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag


class UserResource(resources.ModelResource):
    class Meta:
        model = User
