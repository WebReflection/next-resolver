# next-resolver

[![Coverage Status](https://coveralls.io/repos/github/WebReflection/next-resolver/badge.svg?branch=main)](https://coveralls.io/github/WebReflection/next-resolver?branch=main)

<sup>**Social Media Photo by [Jan Genge](https://unsplash.com/@jan_genge) on [Unsplash](https://unsplash.com/)**</sup>


A utility to simpify the repeated *unique ID* + *promise* dance.

```js
import nextResolver from 'next-resolver';

const [next, resolve] = nextResolver();

// next unique identifier and its promise
const [id, promise] = next();

// pass the promise around, hold the id ...
// ... so that whenever it's done:
if (condition) {
  resolve(id, value);

  // or reject via
  resolve(id, null, new Error('reason'));
}
```

The default `nextResolver()` accepts an optional callback that will receive a unique identifier that can be used to return something else:

```js
// use strings instead of numbers as IDs
const [next, resolve] = nextResolver(String);

const [id, promise] = next();
typeof id; // string

// use any Map key variant
const [next, resolve] = nextResolver(id => {
  // make it stronger (not really useful)
  return `${id}-${crypto.randomUUID()}`;
  // make it a unique ref
  return { id };
});
```

Please note that if the returned value is still awaited, the next `id` will be passed to create a new identifier (so don't put too much logic within the `id` creation, it's already granted to be unique per that logic/session).

This is mostly needed in case you want to brand your async operations, so that something like a prefix would be enough:

```js
const [next, resolve] = nextResolver(id => `my-logic-${id}`);
```

And that's all folks 🥕
