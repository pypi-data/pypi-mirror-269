#ifndef TYPON_TASK_HPP_INCLUDED
#define TYPON_TASK_HPP_INCLUDED

#include <coroutine>
#include <utility>

#include <typon/meta.hpp>
#include <typon/result.hpp>


namespace typon
{

  template <typename T = void>
  struct [[nodiscard]] Task
  {
    struct promise_type;

    std::coroutine_handle<promise_type> _coroutine;

    Task(std::coroutine_handle<promise_type> coroutine) noexcept : _coroutine(coroutine) {
      static_assert(meta::Awaitable<Task>);
    }

    Task(const Task &) = delete;
    Task & operator=(const Task &) = delete;

    Task(Task && other) noexcept
      : _coroutine(std::exchange(other._coroutine, nullptr))
    {}

    Task & operator=(Task other)
    {
      std::swap(_coroutine, other._coroutine);
      return *this;
    }

    ~Task()
    {
      if (_coroutine)
      {
        _coroutine.destroy();
      }
    }

    struct promise_type : Result<T>
    {
      std::coroutine_handle<> _continuation;

      Task get_return_object() noexcept
      {
        return { std::coroutine_handle<promise_type>::from_promise(*this) };
      }

      std::suspend_always initial_suspend() noexcept
      {
        return {};
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

      auto final_suspend() noexcept
      {
        struct awaitable : std::suspend_always
        {
          std::coroutine_handle<> await_suspend(std::coroutine_handle<promise_type> coroutine) noexcept
          {
            return coroutine.promise()._continuation;
          }
        };

        return awaitable {};
      }
    };

    auto operator co_await() && noexcept
    {
      struct awaitable
      {
        std::coroutine_handle<promise_type> _coroutine;

        bool await_ready() noexcept
        {
          return false;
        }

        auto await_suspend(std::coroutine_handle<> continuation) noexcept
        {
          _coroutine.promise()._continuation = continuation;
          return _coroutine;
        }

        decltype(auto) await_resume()
        {
          return _coroutine.promise().get();
        }
      };

      return awaitable { _coroutine };
    }

    auto discard() && noexcept
    {
      struct awaitable : std::suspend_always
      {
        std::coroutine_handle<promise_type> _coroutine;

        std::coroutine_handle<> await_suspend(std::coroutine_handle<> awaiting_coroutine) noexcept
        {
          _coroutine.promise()._continuation = awaiting_coroutine;
          return _coroutine;
        }
      };

      return awaitable { {}, _coroutine };
    }

    decltype(auto) call() &&
    {
      _coroutine.promise()._continuation = std::noop_coroutine();
      _coroutine.resume();
      return _coroutine.promise().get();
    }

    void call_discard() &&
    {
      _coroutine.promise()._continuation = std::noop_coroutine();
      _coroutine.resume();
    }
  };
  
}

#endif // TYPON_TASK_HPP_INCLUDED
