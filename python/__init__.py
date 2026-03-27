import asyncio

__all__ = ["Promise", "next_resolver"]

def resolver(value, wait=True):
  if asyncio.iscoroutine(value):
    task = asyncio.create_task(value)
    if wait:
      async def wait(resolve, reject):
        try:
          resolve(await task)
        except Exception as e:
          reject(e)

      value = Promise(wait)

  return value

class PromiseWithResolvers:
  def __init__(self):
    self.resolve = None
    self.reject = None
    self.promise = None

class Promise(asyncio.Future):

  async def value(promise):
    while isinstance(promise, Promise):
      promise = await promise

    return promise

  def with_resolvers():
    ref = PromiseWithResolvers()

    def fn(resolve, reject):
      ref.resolve = resolve
      ref.reject = reject

    ref.promise = Promise(fn)
    return ref

  def __init__(self, fn):
    super().__init__()
    this = self

    def resolve(value):
      this.set_result(value)

    def reject(reason):
      this.set_exception(reason)

    resolver(fn(resolve, reject), wait=False)

  def then(self, resolve, reject=None):
    p = Promise.with_resolvers()

    def done(future):
      try:
        result = future.result()
        if resolve:
          p.resolve(resolver(resolve(result)))

      except Exception as e:
        if reject:
          p.reject(resolver(reject(e)))

        else:
          raise e

    self.add_done_callback(done)

    return p.promise

  def catch(self, on_rejected):
    return self.then(None, on_rejected)

def next_resolver(typed = int):
  map = {}
  id = 0

  def next():
    nonlocal id

    while True:
      uid = typed(id)
      id += 1

      if id == 2147483648:
        id *= -1

      if not uid in map:
        break

    wr = Promise.with_resolvers()
    map[uid] = wr
    return [uid, wr.promise]

  def resolver(uid, value, error=None):
    if uid in map:
      wr = map[uid]
      del map[uid]

      if error:
        wr.reject(error)
      else:
        wr.resolve(value)

  return [next, resolver]
