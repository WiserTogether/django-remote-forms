# django-remote-forms

A package that allows you to serialize django forms, including fields and widgets into Python
dictionary for easy conversion into JSON and expose over API

Please go through my [djangocon US 2012 talk](http://www.slideshare.net/tarequeh/django-forms-in-a-web-api-world)
to understand the problem sphere, motivations, challenges and implementation of Remote Forms

## Sample Implementation

If you don't mind digging around a little bit to learn about different the components that might be
necessary for an implementation of django-remote-forms, check out
django Remote Admin [django-remote-admin](https://github.com/tarequeh/django-remote-admin)

## Usage

### Minimal Example

```python
from django_remote_forms.forms import RemoteForm

form = LoginForm()
remote_form = RemoteForm(form)
remote_form_dict = remote_form.as_dict()
```

Upon converting the dictionary into JSON, it looks like this:

```json
{
    "is_bound": false,
    "non_field_errors": [],
    "errors": {},
    "title": "LoginForm",
    "fields": {
        "username": {
            "title": "CharField",
            "required": true,
            "label": "Username",
            "initial": null,
            "help_text": "This is your django username",
            "error_messages": {
                "required": "This field is required.",
                "invalid": "Enter a valid value."
            },
            "widget": {
                "title": "TextInput",
                "is_hidden": false,
                "needs_multipart_form": false,
                "is_localized": false,
                "is_required": true,
                "attrs": {
                    "maxlength": "30"
                },
                "input_type": "text"
            },
            "min_length": 6,
            "max_length": 30
        },
        "password": {
            "title": "CharField",
            "required": true,
            "label": "Password",
            "initial": null,
            "help_text": "",
            "error_messages": {
                "required": "This field is required.",
                "invalid": "Enter a valid value."
            },
            "widget": {
                "title": "PasswordInput",
                "is_hidden": false,
                "needs_multipart_form": false,
                "is_localized": false,
                "is_required": true,
                "attrs": {
                    "maxlength": "128"
                },
                "input_type": "password"
            },
            "min_length": 6,
            "max_length": 128
        }
    },
    "label_suffix": ":",
    "prefix": null,
    "csrfmiddlewaretoken": "2M3MDgfzBmkmBrJ9U0MuYUdy8vgeCCgw",
    "data": {
        "username": null,
        "password": null
    }
}
```

### An API endpoint serving remote forms

```python
from django.core.serializers.json import simplejson as json, DjangoJSONEncoder
from django.http import HttpResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt

from django_remote_forms.forms import RemoteForm

from my_awesome_project.forms import MyAwesomeForm


@csrf_exempt
def my_ajax_view(request):
    csrf_middleware = CsrfViewMiddleware()

    response_data = {}
    if request.method == 'GET':
        # Get form definition
        form = MyAwesomeForm()
    elif request.raw_post_data:
        request.POST = json.loads(request.raw_post_data)
        # Process request for CSRF
        csrf_middleware.process_view(request, None, None, None)
        form_data = request.POST.get('data', {})
        form = MyAwesomeForm(form_data)
        if form.is_valid():
            form.save()

    remote_form = RemoteForm(form)
    # Errors in response_data['non_field_errors'] and response_data['errors']
    response_data.update(remote_form.as_dict())

    response = HttpResponse(
        json.dumps(response_data, cls=DjangoJSONEncoder),
        mimetype="application/json"
    )

    # Process response for CSRF
    csrf_middleware.process_response(request, response)
    return response
```

## djangocon Proposal

This is a bit lengthy. But if you want to know more about my motivations behind developing django-remote-forms
then read on.


>In our quest to modularize the architecture of web applications, we create self-containing backend
>systems that provide web APIs for programmatic interactions. This gives us the flexibility to
>separate different system components. A system with multiple backend components e.g. user profile
>engine, content engine, community engine, analytics engine may have a single frontend application
>that fetches data from all of these components using respective web APIs.

>With the increased availability of powerful JavaScript frameworks, such frontend applications are
>often purely JS based to decrease application footprint, increase deployment flexibility and
>separate presentation from data. The separation is very rewarding from a software engineering
>standpoint but imposes several limitations on system design. Using django to construct the API for
>arbitrary consumers comes with the limitation of not being able to utilize the powerful django form
>subsystem to drive forms on these consumers. But is there a way to overcome this restriction?

>This is not a trivial problem to solve and there are only a few assumptions we can make about the
>web API consumer. It can be a native mobile or desktop - application or browser. We advocate that
>web APIs should provide sufficient information about 'forms' so that they can be faithfully
>reproduced at the consumer end.

>Even in a API backend built using django, forms are essential for accepting, filtering, processing
>and saving data. The django form subsystem provides many useful features to accomplish these tasks.
>At the same time it facilitates the process of rendering the form elements in a browser
>environment. The concepts of form fields combined with widgets can go a long way in streamlining
>the interface to interact with data.

>We propose an architecture to serialize information about django forms (to JSON) in a framework
>independent fashion so that it can be consumed by any frontend application that renders HTML. Such
>information includes but is not limited to basic form configurations, security tokens (if
>necessary), rendering metadata and error handling instructions. We lovingly name this architecture
>django-remote-forms.

>At WiserTogether, we are in the process of building a component based architecture that strictly
>provides data endpoints for frontend applications to consume. We are working towards developing
>our frontend application for web browsers using backbone.js as MVC and handlebars as the templating
>engine. django-remote-forms helps us streamline our data input interface with the django forms
>living at the API backend.
