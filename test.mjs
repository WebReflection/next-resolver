import nextResolver from './index.js';

const [nid, nresolve] = nextResolver();

let [id, promise] = nid();
console.assert(typeof id === 'number');
console.assert(promise instanceof Promise);
promise.then(value => {
  console.assert(value === 'number');
});
nresolve(id, 'number');

const [sid, sresolve] = nextResolver(String);
[id, promise] = sid(String);
console.assert(typeof id === 'string');
console.assert(promise instanceof Promise);
promise.then(value => {
  console.assert(value === 'string');
});
sresolve(id, 'string');


[id, promise] = sid(String);
promise.then(
  () => {
    throw new Error('this should not happen');
  },
  error => {
    console.assert(error === 'error');
    console.log('OK');
  }
);
sresolve(id, null, 'error');
