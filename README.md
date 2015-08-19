django-split-json-widget
===

A widget that renders JSON data as separate editable inputs.

## Installation

```pip install django-split-json-widget```
or
```pip install git+https://github.com/abbasovalex/django-SplitJSONWidget-form.git```

### Example №1

#### forms.py

```python
# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget


class testForm(forms.Form):
    attrs = {'class': 'special', 'size': '40'}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
```

#### views.py
```python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import testForm

def test_dict(request):
    json = {'a': 1,
            'b': 2,
            'c': 3,
            'd': 4}
    form = testForm(request.POST or None, initial={'data': json})
    if form.is_valid():
        # validate and save
        pass

    template = 'test_template.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)
```

#### test_template.py
```html
<!doctype html>
<html>
    <head></head>
	<body>
		Errors: 
        {% for field, error in form.errors.items %}
            <ul>
            <li>{{ error }}</li>
            </ul>
        {% empty %}
            no errors 
        {% endfor %}
        <hr/>
        List of:
			<form action="" method="post">
				{% csrf_token %}
				{{ form.as_p}}
				<input type="submit" value="Submit" />
			</form>
	</body>
</html>
```

#### Result (with debug mode enabled)

![simple dict](https://github.com/abbasovalex/django-SplitJSONWidget-form/blob/master/doc/sreenshots/test_dict.png?raw=true)


### Example №2

#### forms.py
```python
# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget


class testForm(forms.Form):
    attrs = {'class': 'special', 'size': '40'}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
```

#### views.py
```python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import testForm

def test_nested_dict(request):
    json = {'a': {'aa': 1},
            'b': [2, 2, {'q': 'qq',
                         'w': 'ww',
                         'z': [1, 2, 3, 4, {'five': 'number',
                                            'six': 'number'}, 7]}],
            'c': 3,
            'd': {'e':'ee', 'f':'ff'},
            'listA': [99, 98, 97, {'text': 'string'}],
            'ListA': [{'name': 'A', 'value': 'No'},
                      {'name': 'B', 'value': 'No'},
                      {'name': 'C', 'value': 'Yes'}]}
    form = testForm(request.POST or None, initial={'data': json})
    if form.is_valid():
        # validate and save
        pass

    template = 'test_template.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)
```

#### test_template.py
```html
<!doctype html>
<html>
	<head></head>
	<body>
		Errors: 
        {% for field, error in form.errors.items %}
            <ul>
            <li>{{ error }}</li>
            </ul>
        {% empty %}
            no errors 
        {% endfor %}
        <hr/>
        List of:
			<form action="" method="post">
				{% csrf_token %}
				{{ form.as_p}}
				<input type="submit" value="Submit" />
			</form>
	</body>
</html>
```

#### Result (debug mode is enabled)

![test](https://github.com/abbasovalex/django-SplitJSONWidget-form/blob/master/doc/sreenshots/test_nested_dict.png?raw=true)



### Example №3

#### forms.py
```python
# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget


class testForm(forms.Form):
    attrs = {'class': 'special', 'size': '40'}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
```

#### views.py
```python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import testForm

def test_list(request):
    json = ['a', 'b', 'c']
    form = testForm(request.POST or None, initial={'data': json})
    if form.is_valid():
        # validate and save
        pass

    template = 'test_template.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)
```

#### test_template.py
```html
<!doctype html>
<html>
	<head></head>
	<body>
		Errors: 
        {% for field, error in form.errors.items %}
            <ul>
            <li>{{ error }}</li>
            </ul>
        {% empty %}
            no errors 
        {% endfor %}
        <hr/>
        List of:
			<form action="" method="post">
				{% csrf_token %}
				{{ form.as_p}}
				<input type="submit" value="Submit" />
			</form>
	</body>
</html>
```

#### Result (debug mode is enabled)

![simple list](https://github.com/abbasovalex/django-SplitJSONWidget-form/blob/master/doc/sreenshots/test_list_.png?raw=true)


### Example №4

#### forms.py
```python
# -*- coding: utf-8 -*-
from django import forms
from splitjson.widgets import SplitJSONWidget


class testForm(forms.Form):
    attrs = {'class': 'special', 'size': '40'}
    data = forms.CharField(widget=SplitJSONWidget(attrs=attrs, debug=True))
```

#### views.py
```python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import testForm

def test_nested_list(request):
    json = [['a', 'b', [1, 2, 3]], {'c': 'best'}, 'd']
    form = testForm(request.POST or None, initial={'data': json})
    if form.is_valid():
        # validate and save
        pass

    template = 'test_template.html'
    context = RequestContext(request, {'form': form})
    return render_to_response(template, context)
```

#### test_template.py
```html
<!doctype html>
<html>
	<head></head>
	<body>
		Errors: 
        {% for field, error in form.errors.items %}
            <ul>
            <li>{{ error }}</li>
            </ul>
        {% empty %}
            no errors 
        {% endfor %}
        <hr/>
        List of:
			<form action="" method="post">
				{% csrf_token %}
				{{ form.as_p}}
				<input type="submit" value="Submit" />
			</form>
	</body>
</html>
```

#### Result (debug mode is enabled)

![nested list](https://github.com/abbasovalex/django-SplitJSONWidget-form/blob/master/doc/sreenshots/test_nested_list%20.png?raw=true)

## Known issues
See https://github.com/abbasovalex/django-SplitJSONWidget-form/issues?labels=bug&page=1&state=open


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/abbasovalex/django-splitjsonwidget-form/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

