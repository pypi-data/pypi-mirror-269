#ifndef TYPON_FORK_HPP_INCLUDED
#define TYPON_FORK_HPP_INCLUDED

#include <atomic>
#include <coroutine>
#include <cstdint>
#include <type_traits>

#include <typon/defer.hpp>
#include <typon/fork_refcount.hpp>
#include <typon/forked.hpp>
#include <typon/meta.hpp>
#include <typon/result.hpp>
#include <typon/scheduler.hpp>
#include <typon/span.hpp>


namespace typon
{

  template <typename T = void>
  struct [[nodiscard]] Fork
  {
    struct promise_type;
    using u64 = Span::u64;

    static constexpr bool is_void { std::is_same_v<T, void> };

    std::coroutine_handle<promise_type> _coroutine;

    Fork(std::coroutine_handle<promise_type> coroutine) noexcept
      : _coroutine(coroutine)
    {
      static_assert(meta::Awaitable<Fork>);
    }

    Fork(const Fork &) = delete;
    Fork& operator=(const Fork &) = delete;

    Fork(Fork &&) noexcept = default;
    Fork& operator=(Fork &&) noexcept = default;

    struct promise_type : Result<T>
    {
      using Refcount = std::conditional_t<is_void, meta::Empty, ForkRefcount>;

      Span * _span;
      [[no_unique_address]] Refcount _refcount;

      Fork get_return_object() noexcept
      {
        return { std::coroutine_handle<promise_type>::from_promise(*this) };
      }

      std::suspend_always initial_suspend() noexcept
      {
        return {};
      }

      auto final_suspend() noexcept
      {
        struct awaitable : std::suspend_always
        {
          std::coroutine_handle<> await_suspend(std::coroutine_handle<promise_type> coroutine) noexcept
          {
            auto span = coroutine.promise()._span;
            auto exception = std::move(coroutine.promise()._exception);
            if constexpr(is_void)
            {
              coroutine.destroy();
            }
            if (Scheduler::pop())
            {
              if (exception)
              {
                span->set_sequential_exception(exception);
                if ((span->_thefts == 0) || span->notify_sync())
                {
                  return span->_continuation;
                }
                return std::noop_coroutine();
              }
              return span->_coroutine;
            }
            if (exception)
            {
              span->set_concurrent_exception(exception);
            }
            if constexpr(!is_void)
            {
              coroutine.promise()._refcount.decref();
            }
            if (span->notify_fork())
            {
              return span->fork_continuation();
            }
            return std::noop_coroutine();
          }
        };

        return awaitable {};
      }
    };

    struct awaitable : std::suspend_always
    {
      std::coroutine_handle<promise_type> _coroutine;
      u64 _thefts;

      awaitable(std::coroutine_handle<promise_type> coroutine)
        : _coroutine(coroutine)
      {}

      template <typename Promise>
      std::coroutine_handle<> await_suspend(std::coroutine_handle<Promise> continuation) noexcept
      {
        Span * span = &(continuation.promise()._span);
        _coroutine.promise()._span = span;
        _thefts = span->_thefts;
        if constexpr(!is_void)
        {
          _coroutine.promise()._refcount.set(_coroutine);
        }
        if (_thefts && span->has_concurrent_exception())
        {
          // Destroy the fork because it will not be run.
          _coroutine.destroy();
          if (span->notify_sync())
          {
            return span->_continuation;
          }
          return std::noop_coroutine();
        }
        std::coroutine_handle<> on_stack_handle = _coroutine;
        Scheduler::push(span);
        return on_stack_handle;
      }

      auto await_resume() noexcept
      {
        if constexpr(!is_void)
        {
          auto span = _coroutine.promise()._span;
          bool ready = (span->_thefts == _thefts);
          return Forked<T>(_coroutine, ready);
        }
      }
    };

    auto operator co_await() &&
    {
      return awaitable { _coroutine };
    }
  };

}

#endif // TYPON_FORK_HPP_INCLUDED
