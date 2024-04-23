#ifndef TYPON_ROOT_HPP_INCLUDED
#define TYPON_ROOT_HPP_INCLUDED

#include <atomic>
#include <coroutine>
#include <cstdint>

#include <typon/result.hpp>
#include <typon/scheduler.hpp>


namespace typon
{

  struct [[nodiscard]] Root
  {
    struct promise_type;

    std::coroutine_handle<promise_type> _coroutine;

    ~Root()
    {
      if (_coroutine.promise()._count.fetch_sub(1) == 1)
      {
        _coroutine.destroy();
      }
    }

    struct promise_type : Result<void>
    {
      std::atomic<std::uint_fast8_t> _count {0};

      Root get_return_object() noexcept
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
          std::atomic<std::uint_fast8_t> & _count;

          void await_suspend(std::coroutine_handle<> coroutine) noexcept
          {
            _count.store(2);
            _count.notify_one();
            if (_count.fetch_sub(1) == 1)
            {
              coroutine.destroy();
            }
          }
        };

        return awaitable { {}, _count };
      }
    };

    void call() &&
    {
      Scheduler::schedule(_coroutine);
      _coroutine.promise()._count.wait(0);
      _coroutine.promise().get();
    }
  };

}

#endif // TYPON_ROOT_HPP_INCLUDED
