from rest_framework.fields import Field
from rest_framework.reverse import reverse

class PkAndUrlReverseField(Field):
    pk_field_name = 'id'
    get_pk = staticmethod(lambda obj: obj.pk)
    get_args = staticmethod(lambda obj: [obj.pk])

    def __init__(self, *args, **kwargs):
        self.pk_field_name = kwargs.pop('pk_field_name', self.pk_field_name)
        self.get_pk = kwargs.pop('get_pk', self.get_pk)
        self.view_name = kwargs.pop('view_name', None)
        self.get_args = kwargs.pop('get_args', self.get_args)

        return super().__init__(*args, **kwargs)

    def to_representation(self, value):
        assert callable(self.get_args), "%s must be a callable" % 'get_args'

        return {
            self.pk_field_name: getattr(self, 'get_pk')(value),
            'url': self.get_url(value)
        }

    def get_url(self, obj):
        assert self.view_name is not None, "%s is required" % 'view_name'

        get_args = getattr(self, 'get_args')

        return reverse(self.view_name, args=get_args(obj), request=self.context['request'])
