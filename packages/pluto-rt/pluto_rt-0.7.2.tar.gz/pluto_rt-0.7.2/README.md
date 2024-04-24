# Pluto-RT: Real-time web results for long-running processes

Any time you have a need to trigger a long-running process from a web view, you run into Python's
blocking nature - nothing will be displayed until the process is complete, and you'll hit timeouts
if you exceed the default timeout for your web application process.

To solve the long-running aspect, we turn to background workers like django-q or django-celery. But
then the user has no insight into what the background worker is doing.

Pluto-RT solves that by using Redis as a message queuing service with a FIFO (first in, first out)
queue. Messages can be placed on the queue by the background worker and when they are retrieved by
the view, it returns the oldest ones first. It can work either by by polling with a WSGI server,
or by using server-sent events (SSE) with ASGI.

![Animated gif showing pluto-rt demo functionality](demo/pluto_rt_demo.gif)

The overall strategy is this:

1. Create a unique "queue name" which can be sent to a worker queue and passed into a "results" page.
1. Invoke your background processor (worker) with that queue name. The worker places messages onto the queue as it progresses with the task.
1. Display the results template, passing it the queue name, item template name and div target. The template generates htmx which retrieves messages associated with that queue.
1. The server removes the oldest messages from the queue and delivers them to the client.

## Demo

There is a demo available in the demo directory. The quickest way to try it out is using docker:

```
docker compose --project-directory demo up
```

Then open your browser to http://localhost:8000/ to view the various demos.

---

Or run with a venv:

```
python3 -m venv .venv
. .venv/bin/activate
.venv/bin/pip install -r demo/requirements.txt
PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=.:src DJANGO_SETTINGS_MODULE=demo.settings .venv/bin/celery -A demo.tasks worker --loglevel=INFO
```

In a new terminal run:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=.:src .venv/bin/granian --reload --interface asginl --port 8000 demo.asgi:application
```

Then open your browser to http://localhost:8000/ to view the various demos.

## Prerequisites

We assume you already have these installed and working

- A running Django project with Redis configured
- A runnning background processor such as celery, with a long-running task defined

## Installation:

- `pip install pluto-rt`
- Add `pluto_rt` to the list of installed apps in project settings.
- Include `pluto_rt.urls` in your project urls.py file (with login_required, etc, if needed). Pick whatever prefix you want.

## Usage

There are two views you'll need to control: the view that kicks off the process
and passes tasks to the background worker, and the view that consumes the results.

After following the installation steps above...

In the launching view:

1. Make the queue name. It should be fairly unique, so that another page load doesn't create the same value. A uuid4 provides for this, plus essentially authorization for the content (the URL would be unguessable):
   ```
   queue_name = f"listqueue_{uuid.uuid4()}"
   ```
1. Launch the long-running process, passing it the queue name:
   ```
   sample_ops_function.delay(queue_name)
   ```
1. Pass the queue name onto the next view (e.g. with a page display or redirect):
   ```
   return render(request, "demo/demo_list.html", {"queue_name": queue_name})
   ```

In the long-running task:

1. Get the queue handle using `pluto_rt.ops.get_rt_queue_handle(queue_name)`. Put messages items onto the queue. The messages must be pickle-able.
   ```
   mqueue = get_rt_queue_handle(queue_name)
   mqueue.push({"status": "info", "msg": "Demo starting"})
   ```
2. When you are finished with the task (successfully or not), call `complete()` on the queue handle.
   ```
   mqueue.complete()
   ```

Create a results template which contains:

1. script elements that load htmx and htmx-sse
1. a target div with an id, which will hold the formatted DOM elements representing each message.
1. the `include` filter loading pluto_rt/sse.html for ASGI servers, or pluto_rt/polling.html for WSGI. Pass in the required `item_template` and `target` parameters, and optionally `mode` (`reverse` or `replace`):

For example:

```
<ul id="results" class="list-group"></ul>
{% include "pluto_rt/sse.html" with item_template="myapp/pluto_rt_item.html" target="#results" %}

<script src="/js/htmx.min.js"></script>
<script src="/js/htmx-sse.min.js"></script>
```

Create an "item" template in your template dirs:

1. The path (directory or filename) of the item_template _must_ contain `pluto_rt`. The format of the template is up to you! The object delivered in the template is named "item", and will hold whatever was added in the long-running process. It is a regular django template item at this point, but it will turn into an HTML snippet before it is delivered to the client. It could be as simple as or as complex as you want, so long as it can be delivered as mime type html/text:

A very simple example:

```
<div>{{ item }}</div>
```

A bit more practical (based on the items added above):

```
<li class="list-group-item list-group-item-{{ item.status }}">{{ item.msg }}</li>
```

We require the path to contain "pluto_rt" as a security measure. Frankly there is little chance that any data might be exposed via a template (the context contains only the `item` variable), but it makes security a little tidier. You can use a path named "pluto_rt", or include it in the template file name.

## Stop polling

If you call `complete()` on the queue, the view will return a message that tells htmx to stop polling. So in your processing function, be sure
to call that function when the work is done.

The default delay between calling `complete()` and having the queue purged is 5 seconds. This can be overridden by passing an int argument (seconds) to `complete()`,
 or via the optional django setting `PLUTO_RT_CLEAR_DELAY`. For testing, this setting should be 0 to prevent slow pytests.

## Distribution and license

Creating this as a private ES github repo first, for re-usability,
with intention to secure permission to open source it in the future.

When this is pip-installed, it will install the wheel, which means you need to recompile the wheel after making changes.

One-time only:

```
pip install build
pip install twine
```

After final commit, change the version in pyproject.toml, then run

`python3 -m build`

Then commit the changes and publish the update to pypi with:

`twine upload dist/pluto_rt-0.1.2.tar.gz`

(replacing the actual build number).

## Versions

0.1.0 Initial version

0.2.0 Sep 1, 2023: Replaced defunct QR3 lib with our own queueing code (made pluto self-sufficient).
    Introduced support for including template partials rather than full-page only.

0.3.0 Dec 14, 2023: Added reverse option, complete() function, demo app.

0.4.0 Feb 21, 2024: Server-sent events, more flexible templates

0.5.0 Mar 3, 2024: Improved template inclusion, added demos

0.6.0 Mar 9, 2024: Use modes, add replace

0.7.0 Apr 9, 2024: Support multiple consumers

0.7.1 Apr 19, 20204: Keepalive every 10 seconds

0.7.2 Apr 23, 20204: Use setting to avoid sleep (for pytest)
