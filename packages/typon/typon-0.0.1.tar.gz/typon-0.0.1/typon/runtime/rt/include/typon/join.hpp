#ifndef TYPON_JOIN_HPP_INCLUDED
#define TYPON_JOIN_HPP_INCLUDED

#include <coroutine>
#include <utility>

#include <typon/meta.hpp>
#include <typon/result.hpp>
#include <typon/span.hpp>


namespace typon
{

  struct [[nodiscard]] Sync {};


  template <typename T = void>
  struct [[nodiscard]] Join
  {
    struct promise_type;

    using coroutine_type = std::coroutine_handle<promise_type>;

    coroutine_type _coroutine;

    Join(coroutine_type coroutine) noexcept : _coroutine(coroutine) {
      static_assert(meta::Awaitable<Join>);
    }

    Join(const Join &) = delete;
    Join & operator=(const Join &) = delete;

    Join(Join && other) noexcept
      : _coroutine(std::exchange(other._coroutine, nullptr))
    {}

    Join & operator=(Join other)
    {
      std::swap(_coroutine, other._coroutine);
      return *this;
    }

    ~Join()
    {
      if (_coroutine)
      {
        _coroutine.destroy();
      }
    }

    struct promise_type : Result<T, meta::Empty>
    {
      using u64 = Span::u64;
      static constexpr u64 UMAX = Span::UMAX;

      Span _span;

      promise_type() noexcept
        : _span(coroutine_type::from_promise(*this))
      {}

      Join get_return_object() noexcept
      {
        return { coroutine_type::from_promise(*this) };
      }

      std::suspend_always initial_suspend() noexcept
      {
        return {};
      }

      void unhandled_exception() noexcept
      {
        _span.set_sequential_exception(std::current_exception());
      }

      template <meta::Awaitable U>
      decltype(auto) await_transform(U && expr) noexcept
      {
        return std::forward<U>(expr);
      }

      template <typename U>
      requires (! meta::Awaitable<U>)
      decltype(auto) await_transform(U && expr) noexcept
      {
        return meta::AwaitReady{std::forward<U>(expr)};
      }

      auto await_transform(Sync &&) noexcept
      {
        struct awaitable
        {
          Span & _span;

          bool await_ready() noexcept
          {
            return (_span._thefts == 0);
          }

          std::coroutine_handle<> await_suspend(coroutine_type coroutine) noexcept
          {
            (void) coroutine;
            if (_span.notify_sync())
            {
              return _span.sync_continuation();
            }
            return std::noop_coroutine();
          }

          void await_resume() noexcept
          {
            _span.reset_sync();
          }
        };

        return awaitable { _span };
      }

      auto final_suspend() noexcept
      {
        struct awaitable : std::suspend_always
        {
          std::coroutine_handle<> await_suspend(coroutine_type coroutine) noexcept
          {
            Span & span = coroutine.promise()._span;
            if ((span._thefts == 0) || span.notify_sync())
            {
              return span._continuation;
            }
            return std::noop_coroutine();
          }
        };

        return awaitable {};
      }
    };

    auto operator co_await() && noexcept
    {
      struct awaitable
      {
        coroutine_type _coroutine;

        bool await_ready() noexcept
        {
          return false;
        }

        auto await_suspend(std::coroutine_handle<> continuation) noexcept
        {
          _coroutine.promise()._span._continuation = continuation;
          return _coroutine;
        }

        decltype(auto) await_resume()
        {
          _coroutine.promise()._span.propagate_exception();
          return _coroutine.promise().value();
        }
      };

      return awaitable { _coroutine };
    }
  };

}

#endif // TYPON_JOIN_HPP_INCLUDED
