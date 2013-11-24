pytanium
========

A front-end web testing tool in Python

Why
---

We need a front-end testing tool that combines the strengths of existing
tools

Comparison
----------

Features not listed below are assumed to be the same among the tools,
ie. cross-browser testing

+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Capability                        | Description                                     | Selenium   | Sahi                       | Watir    | pytanium   |
+===================================+=================================================+============+============================+==========+============+
| Easy HTTPS                        | Auto-accept SSL certs                           | Yes        | Pro only                   | Yes      | Yes        |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Prevent alerts/confirms/prompts   | Doesn't block on these events                   | No         | Yes                        | No       | Yes\*      |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Prevent print                     | Doesn't block on print                          | No         | Yes                        | No       | Yes\*      |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| AJAX waits                        | Waits for AJAX calls to complete                | No         | Yes                        | No       | Yes\*      |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| File downloads                    | Allows files to be saved                        | No         | Yes                        | No       | No         |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Relational identifiers            | Identify objects using in, near, contains etc   | No         | Yes                        | No       | To do      |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Recorder/Object spy               | Easy identification of elements                 | Yes        | Yes                        | No       | Yes        |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Languages                         | Programming languages                           | Many       | JavaScript/Java/Ruby       | Ruby     | Python     |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Cross-domain support              | Consistent cross-domain support                 | Yes        | Occasional configuration   | Yes      | Yes        |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Debugging                         | Breakpoints and introspection                   | Yes        | Sort of\*\*                | Yes      | Yes        |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+
| Technology                        | Browser interaction method                      | Native     | JavaScript events          | Native   | Native     |
+-----------------------------------+-------------------------------------------------+------------+----------------------------+----------+------------+

\*Works as long as the event isn't triggered before the document is
loaded

\*\*Sahi supports running a script line by line. For introspection,
JavaScript must be executed while the script is paused.

How
---

Pytanium uses the `python binding for selenium`_. To provide the
features not typically included with Selenium (AJAX waits, blocking
print calls, etc), pytanium injects javascript on nearly every call to
the browser.

Language Features
-----------------

Pytanium makes it easy to switch from Selenium, Sahi, or Watir. In doing
so, it supports a lot of the same syntax from each of these tools.

Selenium
~~~~~~~~

If you're writing `selenium with python`_ you don't have to change your
existing code, it's syntactically correct pytanium code.

Sahi
~~~~

Pytanium's features are heavily inspired by Sahi, so a lot of Sahi's
syntax works.

Recorder/Object spy
-------------------

Sahi has an excellent object spy and recorder. The pytanium recorder 
leverages this power by simply adding an additional supported
language to Sahi.

`Download the recorder`_

While writing automation, it's helpful to inspect objects on a page
in the same browser instance we're automating. Opening another 
browser just to verify an element on a page is cumbersome and slow.
To use both the recorder and automation simultaneously:

1. Start the Pytanium Recorder (A Sahi Open Source proxy)
2. Pass {'enableRecorder' : True} as one of your capabilities (for Firefox) or desired_capabilities (for everything else)

.. code-block:: python

    from pytanium import webdriver
    
    # For Firefox
    browser = Firefox(capabilities = {'enableRecorder' : True})
    
    # For everything else
    browser = Chrome(desired_capabilities = {'enableRecorder' : True})
    browser = Ie(desired_capabilities = {'enableRecorder' : True})

.. _python binding for selenium: http://selenium.googlecode.com/svn/trunk/docs/api/py/index.html
.. _selenium with python: http://selenium.googlecode.com/svn/trunk/docs/api/py/index.html
.. _Download the recorder: https://github.com/kevlened/Sahi/releases/tag/v1.0

License
-------

LGPL