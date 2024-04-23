=============
RedTurtle Faq
=============

|python| |version| |ci|

.. |python| image:: https://img.shields.io/pypi/pyversions/redturtle.volto.svg
  :target: https://pypi.python.org/pypi/redturtle.faq/

.. |version| image:: http://img.shields.io/pypi/v/redturtle.faq.svg
  :target: https://pypi.python.org/pypi/redturtle.faq

.. |ci| image:: https://github.com/RedTurtle/redturtle.faq/actions/workflows/tests.yml/badge.svg
  :target: https://github.com/RedTurtle/redturtle.faq/actions


Add two new content-types to manage Faqs:

- FaqFolder
- Faq

This product is intended to be a Volto extension, so it only provides the content-types (no custom views or styles).

Faq content-type has **blocks** enabled.


Expandable component
--------------------

FaqFolders have an additional expandable component (@faq-structure) that will return the complete structure of the current context with sub-FaqFolders and Faqs::

    > curl -i http://localhost:8080/Plone/example-folder/@faq-structure -H 'Accept: application/json'


You can also filter faqs querying with **SearchableText** index::

    > curl -i http://localhost:8080/Plone/example-folder/@faq-structure?SearchableText=foo -H 'Accept: application/json'


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install redturtle.faq by adding it to your buildout::

    [buildout]

    ...

    eggs =
        redturtle.faq


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/RedTurtle/redturtle.faq/issues
- Source Code: https://github.com/RedTurtle/redturtle.faq


License
-------

The project is licensed under the GPLv2.
