#ifndef TYPON_META_HPP_INCLUDED
#define TYPON_META_HPP_INCLUDED

#include <coroutine>
#include <type_traits>


namespace typon::meta
{

  struct Empty {};


  template <typename T>
  concept Awaiter = requires (T && a, std::coroutine_handle<void> h)
  {
    // simplified
    a.await_ready();
    a.await_suspend(h);
    a.await_resume();
  };


  /* inspired by and simplified from
     https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1288r0.pdf
   */

  template <typename T>
  concept HasCoAwait = requires (T && a)
  {
    // simplified
    std::forward<T>(a).operator co_await();
  };

  template <typename T>
  concept Awaitable = Awaiter<T> || HasCoAwait<T>;

  template <typename T>
  requires (! Awaitable<T>)
  struct AwaitReady : std::suspend_never {
    T _ready;

    AwaitReady() = delete;
    AwaitReady(const AwaitReady &) = delete;
    AwaitReady & operator=(const AwaitReady &) = delete;

    AwaitReady(T && ready) : _ready(std::move(ready)) {}
    AwaitReady(const T & ready) : _ready(ready) {}

    T await_resume() noexcept {
      return std::move(_ready);
    }
  };


  template <typename T>
  struct AwaitResult_t {
    using type = T;
  };

  template <typename T>
  using AwaitResult = typename AwaitResult_t<T>::type;

  template <Awaiter T>
  struct AwaitResult_t<T> {
    using type = decltype(std::declval<T>().await_resume());
  };

  template <HasCoAwait T>
  struct AwaitResult_t<T> {
    using type = AwaitResult<decltype(std::declval<T>().operator co_await())>;
  };

}


#endif // TYPON_META_HPP_INCLUDED
