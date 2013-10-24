pytanium
========

A front-end web testing tool in Python

Why
---
We need a front-end testing tool that combines the strengths of existing tools

Comparison
-----------
Features not listed below are assumed to be the same among the tools, ie. cross-browser testing

|Capability|Description|Selenium|Sahi|Watir|pytanium|
|:-------------|---------------|-------------|------|-------|-------------|
|Easy HTTPS | Auto-accept SSL certs | Yes | Pro only | Yes | Yes |
|Prevent alerts/confirms/prompts | Doesn't block on these events | No | Yes | No | Yes* |
|Prevent print | Doesn't block on print | No | Yes | No | Yes* |
|AJAX waits | Waits for AJAX calls to complete | No | Yes | No | Yes* |
|File downloads | Allows files to be saved | No | Yes | No | No |
|Relational identifiers | Identify objects using in, near, contains etc| No | Yes | No | Yes |
|Recorder/Object spy | Easy identification of elements | Yes | Yes | No | Yes |
|Languages| Programming languages | Many | JavaScript/Java/Ruby | Ruby | Python |
|Cross-domain support| Consistent cross-domain support | Yes | Occasional configuration | Yes | Yes |
|Debugging | Breakpoints and introspection | Yes | Sort of** | Yes | Yes |
|Technology | Browser interaction method | Native | JavaScript events | Native | Native |


*Works as long as the event isn't triggered before the document is loaded

**Sahi supports running a script line by line. For introspection, JavaScript must be executed while the script is paused.

How
---
Pytanium uses the [python binding for selenium](http://selenium.googlecode.com/svn/trunk/docs/api/py/index.html). To provide the features not typically included with Selenium (AJAX waits, blocking print calls, etc), pytanium injects javascript on nearly every call to the browser. This doesn't have a noticeable impact on performance.

Language Features
-----------------
Pytanium makes it easy to switch from Selenium, Sahi, or Watir. In doing so, it supports a lot of the same syntax from each of these tools.

### Selenium
If you're writing [selenium with python](http://selenium.googlecode.com/svn/trunk/docs/api/py/index.html) you don't have to change your existing code, it's syntactically correct pytanium code.

### Sahi
Pytanium's features are heavily inspired by Sahi, so a lot of Sahi's syntax works.

Recorder/Object spy
-------------------
Sahi has an excellent object spy and recorder. The pytanium recorder is a fork of Sahi Open Source with added pytanium support.
