from rest_framework.fields import Field, ChoiceField, DecimalField
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

class ChoiceDisplayField(ChoiceField):
    """
    ChoiceField that uses the choices' display strings.
    """
    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, display in self.choice_strings_to_values.items():
            if display == data:
                return key

        self.fail('invalid_choice', input=data)

    def _get_choices(self):
        return super()._get_choices()

    def _set_choices(self, choices):
        super()._set_choices(choices)

        # Set the dict to the choices' values rather than keys
        self.choice_strings_to_values = {
            str(key): display for key, display in self.choices.items()
        }

    choices = property(_get_choices, _set_choices)

class AmountField(DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_digits', 15)
        kwargs.setdefault('decimal_places', 2)

        return super().__init__(*args, **kwargs)
