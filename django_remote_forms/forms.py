from django_remote_forms import fields, logger

from django_remote_forms.utils import normalize_errors


class RemoteForm(object):
    def __init__(self, form):
        self.form = form

    def as_dict(self):
        """
        Returns a form as a dictionary that looks like the following:

        form = {
            'non_field_errors': [],
            'label_suffix': ':',
            'is_bound': False,
            'prefix': 'text'.
            'fields': {
                'name': {
                    'type': 'type',
                    'errors': {},
                    'help_text': 'text',
                    'label': 'text',
                    'initial': 'data',
                    'max_length': 'number',
                    'min_length: 'number',
                    'required': False,
                    'bound_data': 'data'
                    'widget': {
                        'attr': 'value'
                    }
                }
            }
        }
        """
        form_dict = {}
        form_dict['non_field_errors'] = normalize_errors(self.form.non_field_errors())
        form_dict['label_suffix'] = self.form.label_suffix
        form_dict['is_bound'] = self.form.is_bound
        form_dict['prefix'] = self.form.prefix
        form_dict['fields'] = {}

        for name, field in self.form.fields.items():
            # Retrieve the initial data from the form itself if it exists so
            # that we properly handle which initial data should be returned in
            # the dictionary.

            # Please refer to the Django Form API documentation for details on
            # why this is necessary:
            # https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
            form_initial_data = getattr(self.form.initial, name, None)

            # Instantiate the Remote Forms equivalent of the field if possible
            # in order to retrieve the field contents as a dictionary.
            try:
                remote_field_class_name = 'Remote%s' % field.__class__.__name__
                remote_field_class = getattr(fields, remote_field_class_name)
                remote_field = remote_field_class(field, form_initial_data)
            except Exception, e:
                logger.warning('Error serializing field %s: %s', remote_field_class_name, str(e))
                field_dict = {}
            else:
                field_dict = remote_field.as_dict()

            form_dict['fields'][name] = field_dict

        return form_dict
