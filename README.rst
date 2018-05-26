=========================
django-codenerix-storages
=========================

Codenerix Storages is a module that enables `CODENERIX <http://www.codenerix.com/>`_ to set storages on several platforms in a general manner

.. image:: http://www.codenerix.com/wp-content/uploads/2018/05/codenerix.png
    :target: http://www.codenerix.com
    :alt: Try our demo with Codenerix Cloud

*********
Changelog
*********

2018-01-17 - Codenerix Storages v1.x is incompatible with v2.x, `what has changed and how to migrate to v2.x? <https://github.com/codenerix/django-codenerix-storages/wiki/Codenerix-Storage-version-1.x-is-icompatible-with-2.x>`_.

****
Demo
****

Coming soon...

**********
Quickstart
**********

1. Install this package::

    For python 2: sudo pip2 install django-codenerix-storages
    For python 3: sudo pip3 install django-codenerix-storages

2. Add "codenerix_storages" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'codenerix_extensions',
        'codenerix_storages',
    ]

3. Add in settings the params::

    # path for codenerix_storages
    CDNX_STORAGES = "storages"
    # Format code for stock movement documents
    CDNX_STORAGE_CODE_REQUEST_STOCK = 'RS{year}{day}{month}-{hour}{minute}--{number}'
    CDNX_STORAGE_CODE_OUTGOING_ALBARAN = 'OA{year}{day}{month}-{hour}{minute}--{number}'
    CDNX_STORAGE_CODE_INGOING_ALBARAN = 'IA{year}{day}{month}-{hour}{minute}--{number}'

4. Since Codenerix Storages is a library, you only need to import its parts into your project and use them.

*************
Documentation
*************

Coming soon... do you help us? `Codenerix <http://www.codenerix.com/>`_

You can chat with us `here <https://goo.gl/NgpzBh>`_.

*******
Credits
*******

This project has been possible thanks to `Centrologic <http://www.centrologic.com/>`_.
