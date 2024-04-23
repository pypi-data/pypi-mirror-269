# Typon concurrency runtime

Typon is a two-part project to bring practical GIL-free concurrency to Python:
1. typon-concurrency (this repository), a C++ concurrency runtime
2. [`typon-compiler`](https://lab.nexedi.com/typon/typon-compiler), a compiler from Python syntax into C++

## `typon/rt`, A Concurrency Runtime

A continuation-stealing concurrency runtime using cutting-edge C++20 coroutines,
featuring both `fork`/`sync` structured concurrency and `future`-based unbounded
concurrency.

### Status

- [x] structured concurrency with `fork`/`sync`
- [x] systematic exception propagation from `fork`ed tasks
- [x] unbounded concurrency with the `future` primitive
- [x] asynchronous waiting on `Future` and `Promise` objects
- [x] mutexes (with asynchronous blocking)
- [x] asynchronous I/O (with [liburing](https://github.com/axboe/liburing))
- [ ] task and I/O cancellation
- [ ] channels

### `fork`/`sync`, Structured Concurrency

```C++
using namespace typon;

Join<int> fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  // Start two potentially concurrent tasks
  Forked a = co_await fork(fibo(n - 1));
  Forked b = co_await fork(fibo(n - 2));
  // Wait until they both complete
  co_await Sync();
  // Access the results
  co_return a.get() + b.get();
}
```

[Structured concurrency](https://en.wikipedia.org/wiki/Structured_concurrency)
is a concurrency paradigm where parallel execution paths are always joined
before exiting the function which created them.

It makes it possible to reason locally about concurrent code, since concurrent
tasks will not outlive the current function. This makes concurrent code more
intuitive and readable, and makes it much easier to reason about memory safety
and thread safety. It also enables systematic exception propagation from
spawned tasks to the parent scope.

The `fork`/`sync` primitives mirror the `spawn`/`sync` paradigm of [Cilk](http://cilk.mit.edu/).

`fork` introduces a potentially parallel nested task. `sync` waits for all
the tasks forked so far in the current scope. `fork`/`sync` can only be used
inside a `Join` coroutine, which guarantees all forked tasks complete before
the parent `Join` coroutine returns, even when there is no explicit `sync`.


### Exception Propagation with `fork`/`sync`

When an exception escapes out of a `fork`, execution of the body of the `Join`
coroutine may have already resumed concurrently and continued past the point
where the `fork` occured.

Therefore propagating an exception from a `fork` is not as easy as in the case
of a simple function call: first the body of the`Join` coroutine must reach a
point where it can stop executing, and then all concurrent forks must complete.

The `Join` coroutine may stop executing at the site of the original `fork` (if
the continuation has not been resumed concurrently), or at any subsequent call
to `fork` after the exception occurs, or at the latest at the next explicit or
implicit `sync`.

Once all concurrent forks have completed, execution jumps directly to the call
site of the `Join` coroutine, where the exception is immediately rethrown as if
the `Join` coroutine had thrown the exception itself.

There is no way to catch that exception directly inside the body of the `Join`
coroutine.

```C++
using namespace typon;

Task<void> throw_exception() {
  // ...
  throw std::exception();
  co_return; // so that this is a coroutine
}

Join<void> parallel() {
  co_await fork(throw_exception());
  // 1. execution may resume concurrently here, or jump straight to 6.

  for (int i = 0; i < 5; i++) {
    // 2. execution may stop abruptly here and jump straight to 6.
    co_await fork(some_task());
  }

  // 3. execution might reach this point

  co_await Sync(); // 4. after this, execution will jump to 6.

  // 5. execution will never reach here
}

Task<void> caller() {
  // ...
  co_await parallel(); // 6. exception is rethrown here

  // ...
}
```


### `future`, A Primitive for Unbounded Concurrency

```
using namespace typon;

Task<int> fibo(int n) {
  if (n < 2) {
    co_return n;
  }
  // Start two potentially concurrent tasks
  Future a = co_await future(fibo(n - 1));
  Future b = co_await future(fibo(n - 2));
  // Wait for each future and retrieve the results
  co_return co_await a.get() + co_await b.get();
}
```

In cases when structured concurrency is too constraining, the `future` primitive
creates concurrent tasks that may outlive the parent scope, more like the `go`
statement in Go. Unlike `go`, `future` immediately returns a `Future` object
that can be used to wait for the task to complete. If the `Future` object is
not used, the task becomes "detached" and lives independantly.


### Examples

See `rt/examples`.


### Using `rt/typon`

`typon/rt` is a headers-only library, so no preliminary build step is required.
Programs only need to include `rt/include/typon/typon.hpp`.

Compiling requires a compiler supporting C++20, such as `gcc++-11` or
`clang++-14` or more recent.

See `rt/examples` for compilation flags.


### References

##### Structured Concurrency

- Nathaniel J. Smith's [Notes on structured concurrency](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)

- Martin Sústrik's blog articles on [structured concurrency](https://250bpm.com/blog:137/index.html)

- Lewis Baker's talk on [structured concurrency with C++20 coroutines](https://www.youtube.com/watch?v=1Wy5sq3s2rg)


##### C++20 Coroutines

- Lewis Baker's [Asymmetric Transfer blog on C++20 coroutines](https://lewissbaker.github.io/)

- [C++20 coroutines at cppreference.com](https://en.cppreference.com/w/cpp/language/coroutines)


##### Papers

- N. S. Arora, R. D. Blumofe, and C. G. Plaxton. 1998.
  Thread scheduling for multiprogrammed multiprocessors.
  https://doi.org/10.1145/277651.277678

- D. Chase and Y. Lev. 2005.
  Dynamic circular work-stealing deque.
  https://doi.org/10.1145/1073970.1073974

- N. M. Lê, A. Pop, A. Cohen, and F. Zappa Nardelli. 2013.
  Correct and efficient work-stealing for weak memory models.
  https://doi.org/10.1145/2517327.2442524

- Kyle Singer, Yifan Xu, and I-Ting Angelina Lee. 2019.
  Proactive work stealing for futures.
  https://doi.org/10.1145/3293883.3295735

- C. X. Lin, T .W Huang, and M. D. F. Wong. 2020.
  An efficient work-stealing scheduler for task dependency graph.
  https://tsung-wei-huang.github.io/papers/icpads20.pdf

- F. Schmaus, N. Pfeiffer, W. Schröder-Preikschat, T. Hönig, and J. Nolte.
    2021. Nowa: a wait-free continuation-stealing concurrency platform.
          https://www4.cs.fau.de/Publications/2021/schmaus2021nowa.pdf


### References

##### Language Design

- Abilian's [design note on syntax for a Python-derived language](https://github.com/abilian/cythonplus-sandbox/blob/devel/sandbox/comparison.md)


##### Technical References

- Python's [`ast` module](https://docs.python.org/3/library/ast.html)

- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)

- [PEP 526 – Syntax for Variable Annotations](https://peps.python.org/pep-0526/)


##### Related Works

- Lukas Martinelli's [`py14` project](https://github.com/lukasmartinelli/py14)

- [The `py2many` project](https://github.com/py2many/py2many)

- [`mypyc`](https://github.com/mypyc/mypyc)

- [`mycpp`, a Python to C++ translator](https://www.oilshell.org/blog/2022/05/mycpp.html)



## `typon/bindings`, Python/C++ bindings for Typon

### Status

This part has not been started yet.


### Driving Idea

The previous part `typon/compiler`, aims to produce a language that takes
Python syntax as input, but is otherwise completely independent of Python.

Using Python/C++ bindings, this language can be made to be interoperable
with true Python, allowing it to be called from standard Python and to call
standard Python code.

Using the first part `typon/rt`, concurrent code may acquire the Python GIL
asynchronously so as not to block the underlying worker thread, in order to
safely call standard Python code.


### References

##### Technical References

- [The Python Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock)


##### Related Works

- [`nanobind`, a C++17/Python bindings library](https://github.com/wjakob/nanobind)

- [`pybind11`, a C++11/Python bindings library](https://github.com/pybind/pybind11)

- [Cython](https://cython.org/)

- [The Cython+ project](https://www.cython.plus/)

- [`mypyc`](https://github.com/mypyc/mypyc)
