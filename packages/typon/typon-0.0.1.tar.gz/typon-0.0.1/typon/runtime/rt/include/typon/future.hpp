#ifndef TYPON_FUTURE_HPP_INCLUDED
#define TYPON_FUTURE_HPP_INCLUDED

#include <atomic>
#include <coroutine>
#include <cstdint>
#include <utility>

#include <typon/meta.hpp>
#include <typon/result.hpp>
#include <typon/scheduler.hpp>
#include <typon/stack.hpp>
#include <typon/theft_point.hpp>


namespace typon
{

  template <typename T = void>
  struct [[nodiscard]] Future
  {
    struct promise_type;

    using enum std::memory_order;

    static constexpr std::uintptr_t no_waiter {0};
    static constexpr std::uintptr_t ready {1};
    static constexpr std::uintptr_t discarded {2};

    std::coroutine_handle<promise_type> _coroutine;
    bool _ready = false;

    Future(std::coroutine_handle<promise_type> coroutine) noexcept
      : _coroutine(coroutine)
    {}

    Future(const Future &) = delete;
    Future& operator=(const Future &) = delete;

    Future(Future && other) noexcept
      : _coroutine(std::exchange(other._coroutine, nullptr))
      , _ready(other._ready)
    {}

    Future & operator=(Future other) noexcept
    {
      std::swap(_coroutine, other._coroutine);
      std::swap(_ready, other._ready);
      return *this;
    }

    ~Future()
    {
      if (_coroutine)
      {
        if (_ready)
        {
          _coroutine.destroy();
        }
        else
        {
          auto state =_coroutine.promise()._state.exchange(discarded, acq_rel);
          if (state == ready)
          {
            _coroutine.destroy();
          }
        }
      }
    }

    struct Continuation : TheftPoint
    {
      std::coroutine_handle<> _continuation;

      std::coroutine_handle<> steal() noexcept override
      {
        return std::exchange(_continuation, nullptr);
      }

      operator std::coroutine_handle<>() noexcept
      {
        return _continuation;
      }

      bool ready() noexcept
      {
        return bool(_continuation);
      }
    };

    struct promise_type : Result<T>
    {
      std::atomic<std::uintptr_t> _state { no_waiter };

      Future get_return_object() noexcept
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
            auto theftpoint = Scheduler::peek();
            if (Scheduler::pop())
            {
              return *static_cast<Continuation *>(theftpoint);
            }
            auto state = coroutine.promise()._state.exchange(ready, acq_rel);
            if (state == discarded)
            {
              coroutine.destroy();
            }
            else
            {
              if (state > 2)
              {
                Scheduler::enable(reinterpret_cast<Stack *>(state));
              }
            }
            return std::noop_coroutine();
          }
        };

        return awaitable {};
      }
    };

    auto operator co_await() &&
    {
      struct awaitable
      {
        Future _future;
        std::coroutine_handle<promise_type> _coroutine;
        Continuation _continuation;

        awaitable(Future && f, std::coroutine_handle<promise_type> c) noexcept
          : _future(std::move(f))
          , _coroutine(c)
        {}

        bool await_ready() noexcept
        {
          return false;
        }

        auto await_suspend(std::coroutine_handle<> continuation) noexcept
        {
          _continuation._continuation = continuation;

          std::coroutine_handle<> on_stack_handle = _coroutine;
          Scheduler::push(&(_continuation));
          return on_stack_handle;
        }

        auto await_resume() noexcept
        {
          _future._ready = _continuation.ready();
          return std::move(_future);
        }
      };
      return awaitable { std::move(*this), _coroutine };
    }

    auto get()
    {
      struct awaitable
      {
        std::coroutine_handle<promise_type> _coroutine;
        bool & _ready;

        bool await_ready() noexcept
        {
          return _ready || _coroutine.promise()._state.load(acquire) == ready;
        }

        void await_suspend(std::coroutine_handle<> continuation) noexcept
        {
          auto stack = Scheduler::suspend(continuation);
          auto state = reinterpret_cast<std::uintptr_t>(stack);
          if (_coroutine.promise()._state.exchange(state, acq_rel) == ready)
          {
            Scheduler::enable(stack);
          }
        }

        auto await_resume()
        {
          return _coroutine.promise().get();
        }
      };

      return awaitable { _coroutine, this->_ready };
    }
  };
}


#endif // TYPON_FUTURE_HPP_INCLUDED
