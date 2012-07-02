class RemoteField(object):
    """
    A base object for being able to return a field as a dictionary.

    It also takes into account if there is initial data for the field coming in
    from the form directly, which overrides any initial data specified on the
    field per Django's rules:

    https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    """

    def __init__(self, field, initial_data=None):
        self.field = field
        self.initial_data = initial_data

    def as_dict(self):
        return {
            'required': self.field.required,
            'widget': None,  # TODO:  Get widget as_dict() working.
            'label': self.field.label,
            'initial': self.initial_data or self.field.initial,
            'help_text': self.field.help_text,
            'error_messages': self.field.error_messages,
        }


class RemoteCharField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteCharField, self).as_dict()

        field_dict.update(
            max_length=self.field.max_length,
            min_length=self.field.min_length
        )

        return field_dict


class RemoteIntegerField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteIntegerField, self).as_dict()

        field_dict.update(
            max_value=self.field.max_value,
            min_value=self.field.min_value
        )

        return field_dict


class RemoteFloatField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteFloatField, self).as_dict()

        field_dict.update(
            max_value=self.field.max_value,
            min_value=self.field.min_value
        )

        return field_dict


class RemoteDecimalField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteDecimalField, self).as_dict()

        field_dict.update(
            max_value=self.field.max_value,
            min_value=self.field.min_value,
            max_digits=self.field.max_digits,
            decimal_places=self.field.decimal_places
        )

        return field_dict


class RemoteDateField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteDateField, self).as_dict()

        field_dict.update(input_formats=self.field.input_formats)

        return field_dict


class RemoteTimeField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteTimeField, self).as_dict()

        field_dict.update(input_formats=self.field.input_formats)

        return field_dict


class RemoteDateTimeField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteDateTimeField, self).as_dict()

        field_dict.update(input_formats=self.field.input_formats)

        return field_dict


class RemoteRegexField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteRegexField, self).as_dict()

        field_dict.update(
            regex=self.field.regex,
            max_length=self.field.max_length,
            min_length=self.field.min_length
        )

        return field_dict


class RemoteChoiceField(RemoteField):
    def as_dict(self):
        field_dict = super(RemoteChoiceField, self).as_dict()

        field_dict.update(choices=self.field.choices)

        return field_dict
