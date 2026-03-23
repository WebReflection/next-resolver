# next-resolver (Python)

A utility to simplify the repeated **unique ID** + **async promise** pattern, built on [`asyncio`](https://docs.python.org/3/library/asyncio.html).

Install from [PyPI](https://pypi.org/project/next-resolver/):

```bash
pip install next-resolver
```

## Basic usage

```python
from next_resolver import next_resolver

next_fn, resolve = next_resolver()

# next unique identifier and its awaitable
uid, promise = next_fn()

# pass `promise` around, keep `uid` …
# … then when the work is done:
if condition:
    resolve(uid, value)

# or reject:
if error:
    resolve(uid, None, error=ValueError("reason"))
```

`promise` is a `Promise` (subclass of `asyncio.Future`). Await it like any other future:

```python
result = await promise
```

## Custom ID types

The factory accepts a callable `typed` (default: `int`) that turns a running counter into an ID. Use `str` for string IDs, or any hashable value suitable for use as a dict key:

```python
next_fn, resolve = next_resolver(str)

uid, promise = next_fn()
assert isinstance(uid, str)
```

```python
next_fn, resolve = next_resolver(lambda n: f"job-{n}")

uid, promise = next_fn()
```

If the callable can still collide with an existing ID, the implementation increments and tries again until the ID is unused—so keep ID creation cheap and deterministic per counter value.

## `Promise`

`Promise` extends `asyncio.Future` and adds chaining similar to JavaScript promises:

- `then(on_fulfilled, on_rejected=None)` — returns another `Promise`
- `catch(on_rejected)` — rejection-only handler

Nested `Promise` values can be flattened with the async helper `Promise.value(promise)`.

## Requirements

Python 3.8+

## See also

The [repository README](https://github.com/WebReflection/next-resolver#readme) documents the JavaScript package of the same name.
