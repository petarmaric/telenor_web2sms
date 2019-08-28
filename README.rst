IMPORTANT NOTICE
================

This project has been retired. Please contact its author if you wish to take
over its maintenance.

Installation
============

To install telenor_web2sms run::

    $ pip install telenor_web2sms


Console app usage
=================

Quick start::

    $ telenor_web2sms

Show help::

    $ telenor_web2sms --help


Python API usage
================

Quick start::

    >>> from telenor_web2sms import TelenorWeb2SMS
    >>> web2sms = TelenorWeb2SMS('username', 'password') # Authenticate
    >>> web2sms.send_sms('phone_number', 'message') # Send SMS


Contribute
==========

If you find any bugs, or wish to propose new features `please let me know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to AUTHORS_.


.. _`please let me know`: https://bitbucket.org/petar/telenor_web2sms/issues/new
.. _`the repository`: http://bitbucket.org/petar/telenor_web2sms
.. _AUTHORS: https://bitbucket.org/petar/telenor_web2sms/src/default/AUTHORS


New in telenor_web2sms 1.0.2
============================

    * Minor tweak in README.
