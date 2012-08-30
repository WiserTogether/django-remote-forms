import datetime

from django.utils.datastructures import SortedDict

from django_remote_forms import logger, widgets
from django_remote_forms.utils import normalize_errors


class RemoteField(object):
    """
    A base object for being able to return a Django Form Field as a Python
    dictionary.

    This object also takes into account if there is initial data for the field
    coming in from the form directly, which overrides any initial data
    specified on the field per Django's rules:

    https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    """

    def __init__(self, field, form_initial_data=None, field_name=None):
        self.field_name = field_name
        self.field = field
        self.form_initial_data = form_initial_data

    def as_dict(self):
        field_dict = SortedDict()
        field_dict['title'] = self.field.__class__.__name__
        field_dict['required'] = self.field.required
        field_dict['label'] = unicode(self.field.label)
        field_dict['initial'] = self.form_initial_data or self.field.initial
        field_dict['help_text'] = unicode(self.field.help_text)

        field_dict['error_messages'] = normalize_errors(self.field.error_messages)

        # Instantiate the Remote Forms equivalent of the widget if possible
        # in order to retrieve the widget contents as a dictionary.
        remote_widget_class_name = 'Remote%s' % self.field.widget.__class__.__name__
        try:
            remote_widget_class = getattr(widgets, remote_widget_class_name)
            remote_widget = remote_widget_class(self.field.widget, field_name=self.field_name)
        except Exception, e:
            logger.warning('Error serializing %s: %s', remote_widget_class_name, str(e))
            widget_dict = {}
        else:
            widget_dict = remote_widget.as_dict()

        field_dict['widget'] = widget_dict

        return field_dict


class RemoteCharField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteCharField, self).as_dict()

        field_dict.update({
            'max_length': self.field.max_length,
            'min_length': self.field.min_length
        })

        return field_dict


class RemoteIntegerField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteIntegerField, self).as_dict()

        field_dict.update({
            'max_value': self.field.max_value,
            'min_value': self.field.min_value
        })

        return field_dict


class RemoteFloatField(RemoteIntegerField):
    def as_dict(self):
        return super(RemoteFloatField, self).as_dict()


class RemoteDecimalField(RemoteIntegerField):
    def as_dict(self):
        field_dict = super(RemoteDecimalField, self).as_dict()

        field_dict.update({
            'max_digits': self.field.max_digits,
            'decimal_places': self.field.decimal_places
        })

        return field_dict


class RemoteTimeField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteTimeField, self).as_dict()

        field_dict['input_formats'] = [unicode(x) for x in self.field.input_formats]

        if (field_dict['initial']):
            if callable(field_dict['initial']):
                field_dict['initial'] = field_dict['initial']()

            if (isinstance(field_dict['initial'], (datetime.datetime, datetime.time, datetime.date))):
                field_dict['initial'] = field_dict['initial'].strftime(field_dict['input_formats'][0])

        return field_dict


class RemoteDateField(RemoteTimeField):
    def as_dict(self):
        return super(RemoteDateField, self).as_dict()


class RemoteDateTimeField(RemoteTimeField):
    def as_dict(self):
        return super(RemoteDateTimeField, self).as_dict()


class RemoteRegexField(RemoteCharField):
    def as_dict(self):
        field_dict = super(RemoteRegexField, self).as_dict()

        field_dict['regex'] = self.field.regex

        return field_dict


class RemoteEmailField(RemoteCharField):
    def as_dict(self):
        return super(RemoteEmailField, self).as_dict()


class RemoteFileField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteField, self).as_dict()

        field_dict['max_length'] = self.field.max_length

        return field_dict


class RemoteImageField(RemoteFileField):
    def as_dict(self):
        return super(RemoteImageField, self).as_dict()


class RemoteURLField(RemoteCharField):
    def as_dict(self):
        return super(RemoteURLField, self).as_dict()


class RemoteBooleanField(RemoteField):
    def as_dict(self):
        return super(RemoteBooleanField, self).as_dict()


class RemoteNullBooleanField(RemoteBooleanField):
    def as_dict(self):
        return super(RemoteNullBooleanField, self).as_dict()


class RemoteChoiceField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteChoiceField, self).as_dict()

        field_dict['choices'] = []
        for key, value in self.field.choices:
            field_dict['choices'].append({
                'value': key,
                'display': value
            })

        return field_dict


class RemoteTypedChoiceField(RemoteChoiceField):
    def as_dict(self):
        field_dict = super(RemoteTypedChoiceField, self).as_dict()

        field_dict.update({
            'coerce': self.coerce,
            'empty_value': self.empty_value
        })

        return field_dict


class RemoteMultipleChoiceField(RemoteChoiceField):
    def as_dict(self):
        return super(RemoteMultipleChoiceField, self).as_dict()


class RemoteModelMultipleChoiceField(RemoteMultipleChoiceField):
    def as_dict(self):
        return super(RemoteModelMultipleChoiceField, self).as_dict()


class RemoteTypedMultipleChoiceField(RemoteMultipleChoiceField):
    def as_dict(self):
        field_dict = super(RemoteTypedMultipleChoiceField, self).as_dict()

        field_dict.update({
            'coerce': self.coerce,
            'empty_value': self.empty_value
        })

        return field_dict


class RemoteComboField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteComboField, self).as_dict()

        field_dict.update(fields=self.field.fields)

        return field_dict


class RemoteMultiValueField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteMultiValueField, self).as_dict()

        field_dict.update(fields=self.field.fields)

        return field_dict


class RemoteFilePathField(RemoteChoiceField):
    def as_dict(self):
        field_dict = super(RemoteFilePathField, self).as_dict()

        field_dict.update({
            'path': self.field.path,
            'match': self.field.match,
            'recursive': self.field.recursive
        })

        return field_dict


class RemoteSplitDateTimeField(RemoteMultiValueField):
    def as_dict(self):
        field_dict = super(RemoteSplitDateTimeField, self).as_dict()

        field_dict.update({
            'input_date_formats': self.field.input_date_formats,
            'input_time_formats': self.field.input_time_formats
        })

        return field_dict


class RemoteIPAddressField(RemoteCharField):
    def as_dict(self):
        return super(RemoteIPAddressField, self).as_dict()


class RemoteSlugField(RemoteCharField):
    def as_dict(self):
        return super(RemoteSlugField, self).as_dict()
