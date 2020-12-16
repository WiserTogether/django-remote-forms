from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.forms.models import ModelChoiceIteratorValue
from django.db import models

def resolve_promise(o):
    if isinstance(o, dict):
        for k, v in o.items():
            o[k] = resolve_promise(v)
            if isinstance(o[k], ModelChoiceIteratorValue):
                o[k] = getattr(o[k], 'value')
    elif isinstance(o, (list, tuple)):
        o = [resolve_promise(x) for x in o]
    elif isinstance(o, Promise):
        try:
            o = force_text(o)
        except:
            # Item could be a lazy tuple or list
            try:
                o = [resolve_promise(x) for x in o]
            except:
                raise Exception('Unable to resolve lazy object %s' % o)
    elif callable(o):
        o = o()
    elif isinstance(o, models.Model): # New treatment for models instances, return the model instance id
        try:
            o = o.id
        except Exception as e:
            print(e)
    return o
