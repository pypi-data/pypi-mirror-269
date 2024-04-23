[![Build Status](https://travis-ci.com/agua-man/blended-python.svg?token=yfkzqqh28cQrdKDkFuFp&branch=master)](https://travis-ci.com/agua-man/blended-python)

==================
**blended-python**
==================

~~~~~~~~~~~~~~~~~~~~~~~~~~~

======
jinja
======

How to use blended-python in jinja:
-------------------------

Create a virtualenv

python2:
::
	$ virtualenv -p python2.7 jinjaenv

python3:
::
	$ virtualenv -p python3.4 jinjaenv

Activate virtualenv and install jinja2
::
	$ cd jinjaenv/

	$ source bin/activate

	$ pip install jinja2==2.8 

Install blended-python
::
	$ pip install http://52.0.54.5/blended-2.0.1.tar

In your jinja code, in order to use blended-python replace
::
        from jinja2 import Environment

with
::
        from blendedUxLang.blended.jinjaenv import BlendedEnvironment as Environment

How to run blended-python tests:
-------------------------
Install pytest library in virtualenv:
::
	$ pip install pytest

Clone blended-lang tests from bitbucket:
::
	$ git clone https://username@bitbucket.org/blendedux/blended-lang-tests.git


Run Tests:
::
	$ cd blended-lang-test/

        $ git checkout new_tests_file_structure
      
        $ cd blended-jinja-tests/

	$ python testrunner.py


How to run Jinja built-in tests with blended-python:
--------------------------------

Clone entire blended-python repo from github:
::
	$ git clone https://username@bitbucket.org/blendedux/blended-python.git

To run Jinja built-in tests
::      
        $ cd blended-python/tests/jinja/
     
        $ py.test




~~~~~~~~~~~~~~~~~~~~~~~~~~~




======
Flask
======

How to use blended-python in flask:
-------------------------

Create a virtualenv

python2:
::
	$ virtualenv -p python2.7 flaskenv

python3:
::
	$ virtualenv -p python3.4 flaskenv

Activate virtualenv and install flask
::
	$ cd flaskenv/

	$ source bin/activate

	$ pip install flask==0.10.1  

Install blended-python
::
	$ pip install http://52.0.54.5/blended-2.0.1.tar

In your flask code, in order to use blended-python replace
::
	import flask

with
::
	from blendedUxLang.blended.flask import Flask

	setattr(flask, 'Flask', Flask) 

and replace
::
	from flask import Flask

with
::
	from blendedUxLang.blended.flask import Flask


How to run Flask built-in tests with blended-python:
--------------------------------

Clone entire blended-python repo from github:
::
	$ git clone https://username@bitbucket.org/blendedux/blended-python.git

To run Flask built-in tests
::      
        $ cd blended-python/tests/flask
     
        $ python run-flask-tests.py




~~~~~~~~~~~~~~~~~~~~~~~~~




======
Django
======

How to use blended-python in django:
-------------------------

Create a virtualenv

python2:
::
	$ virtualenv -p python2.7 djangoenv

python3:
::
	$ virtualenv -p python3.4 djangoenv

Activate virtualenv and install djangoenv
::
	$ cd djangoenv/

	$ source bin/activate

	$ pip install Django==1.8.5

        $ pip install jinja2==2.8  

Install blended-python
::
	$ pip install http://52.0.54.5/blended-2.0.1.tar

Install customtags library
::
	$ pip install http://52.0.54.5/django-customtags-lib-0.1.alpha.tar

In your Django settings file add customtags and djangotags to INSTALLED_APPS
::
  INSTALLED_APPS = (
        ...
        customtags,
        blended.djangotags,
  )

Then add blended_context_processor to TEMPLATES->OPTIONS->context_processors
::
  TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'blended.djangocontext.blended_context_processor',
            ],
        },
    },
  ]


How to run blended-python tests:
-------------------------
Install pytest library in virtualenv:
::
	$ pip install pytest

Clone blended-lang tests from bitbucket:
::
	$ git clone https://username@bitbucket.org/blendedux/blended-lang-tests.git
 
        $ cd blended-lang-tests/
	
	$ git checkout new_tests_file_structure

	$ cd blended-django-tests/

Run Tests with jinja2 Template engine in django:
::
	
	$ python manage.py test blendedtestapp.tests_jinja

Run Tests with django Template engine in django:
::
	
	$ python manage.py test blendedtestapp.tests_django


How to run Django built-in tests with blended-python:
--------------------------------

Clone entire blended-python repo from github:
::
	$ git clone https://username@bitbucket.org/blendedux/blended-python.git

Install mock library
::
        $ pip install mock

To run Django built-in tests
::      
        $ cd blended-python/tests/djangotests/
     
        $ ./runtests.py template_tests



Include jinja Environment in Django:
--------------------------

Open settings.py module of the django project:

::  

	$ vim path/to/project_name/to/settings.py

Include 'Backend' and 'environment option' settings for jinja template engine in TEMPLATE variable of settings file:

::

	TEMPLATE=[
	            {
	             'BACKEND': 'django.template.backends.jinja2.Jinja2',
	             'DIRS': [
	                  '/path/to/jinja2_supportable_syntax_template/',
	                 ],
	             'OPTIONS':{
	                   'environment':'blended.djangotags.django-jinjaenv.environment', 
                           'autoescape': False,     
	                 },
	             },
	             {
	              #other backend settings and options............. 
	             },
         	]

Note: *'autoescape' option must be false for template special characters for example if autoescape is 'True' : '&&' is render as '&amp;' if it is false '&&' is render as '&&'*

**Use of 'static' and 'url' when jinja template engine is on in django:**

In django template engine we can use static in templates, Example like:

::

	<link rel="stylesheet" type ="text/css" href="{% static 'app_name/style.css' %}"/>
	<a href = "{% url 'app_name:view_name' question.id %}">
   

by using {% load staticfiles %} tag.

**BUT**

When we use jinja Template engine we use 'static' and 'url' as functions instead of tags Example like:

::

	<link rel="stylesheet" type ="text/css" href="{{ static('app_name/style.css') }}"/>
	<a href = "{{ url('app_name:view_name', question.id) }}">



Since, we can use jinja template engine in django1.8 jinja don't know about the context_processors of django so we can't use RequestContext to load a jinja template.

To make template object with blended Environment object we can use this:

::
     
	from django.templates import engines

	template = engines['jinja2'].env.get_template(template_name)
     
	or
     
	template = engines['jinja2'].env.from_string(template_string)


**Example of django view rendering template with jinja syntax:** 

::

	from django.shortcuts import render_to_response

	def view_func(request):
  	    context = {}
            return render_to_response('index.html', context)

	or 
      
	from django.shortcuts import render
     
	def view_func(request):
           context = {}
           return render(request, 'index.html', context)
