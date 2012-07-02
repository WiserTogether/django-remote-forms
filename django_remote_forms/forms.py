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
                }
            }
        }

        This allows one to fully reconstruct the form as needed.
        """

        form_dict = {}
        form_dict['non_field_errors'] = self.form.non_field_errors()
        form_dict['label_suffix'] = self.form.get('label_suffix', None)
        form_dict['is_bound'] = self.form.get('is_bound', False)
        form_dict['prefix'] = self.form.get('prefix', None)
        form_dict['fields'] = {}

        for name, field in self.form.fields.items():
            form_dict['fields'][name] = {}  # TODO:  Call field.as_dict()

        return form_dict
