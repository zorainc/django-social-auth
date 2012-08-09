Integration Tests
=================

Integration tests using PhantomJS_ and CasperJS_.


Dependencies
------------

The tests depend on PhantomJS_ and CasperJS_, also settings are needed to fill
the needed credentials to run the tests in the diferent providers.

- Install PhantomJS_ and CasperJS_ following the guides in their sites.

- Copy ``settings.template.js`` as ``settings.js`` and fill the needed values.

- Run the example application attached to django-social-auth_ (further
  customizations will be added to run the tests against any project).

- Run each provider setting using (an scrip to run them all will be added
  later)::

  $ casper <file>.js
  

.. _PhantomJS: http://phantomjs.org/
.. _CasperJS: http://casperjs.org/
.. _django-social-auth: https://github.com/omab/django-social-auth/tree/master/example
