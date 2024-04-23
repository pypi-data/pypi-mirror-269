#ifndef TYPON_PROMISE_HPP_INCLUDED
#define TYPON_PROMISE_HPP_INCLUDED

#include <atomic>
#include <cstdint>
#include <memory>
#include <type_traits>

#include <typon/defer.hpp>
#include <typon/stack.hpp>
#include <typon/scheduler.hpp>


namespace typon
{

  template <typename T>
  struct Promise
  {
    static constexpr std::uintptr_t ready {0};
    static constexpr std::uintptr_t no_waiter {1};

    std::atomic_uintptr_t _state {no_waiter};
    bool _consumed {false};
    union
    {
      T _value;
    };

    ~Promise()
    {
      if (!_consumed)
      {
        if (_state.load(std::memory_order_acquire) == ready)
        {
          std::destroy_at(std::addressof(_value));
        }
      }
    }

    void put(T value)
    {
      std::construct_at(std::addressof(_value), std::move(value));
      auto state = _state.exchange(ready, std::memory_order_acq_rel);
      if (state != no_waiter)
      {
        Scheduler::enable(reinterpret_cast<Stack *>(state));
      }
    }

    bool await_ready() noexcept
    {
      return _state.load(std::memory_order_acquire) == ready;
    }

    void await_suspend(std::coroutine_handle<> coroutine) noexcept
    {
      auto stack = Scheduler::suspend(coroutine);
      auto state = reinterpret_cast<std::uintptr_t>(stack);
      if (_state.exchange(state, std::memory_order_acq_rel) == ready)
      {
        Scheduler::enable(stack);
      }
    }

    T await_resume() noexcept
    {
      Defer defer( [this]() { std::destroy_at(std::addressof(_value)); });
      _consumed = true;
      return std::move(_value);
    }
  };


  template <typename T>
    requires std::is_trivially_destructible_v<T>
  struct Promise<T>
  {
    static constexpr std::uintptr_t ready {0};
    static constexpr std::uintptr_t no_waiter {1};

    std::atomic_uintptr_t _state {no_waiter};
    union
    {
      T _value;
    };

    void put(T value)
    {
      std::construct_at(std::addressof(_value), std::move(value));
      auto state = _state.exchange(ready, std::memory_order_acq_rel);
      if (state != no_waiter)
      {
        Scheduler::enable(reinterpret_cast<Stack *>(state));
      }
    }

    bool await_ready() noexcept
    {
      return _state.load(std::memory_order_acquire) == ready;
    }

    void await_suspend(std::coroutine_handle<> coroutine) noexcept
    {
      auto stack = Scheduler::suspend(coroutine);
      auto state = reinterpret_cast<std::uintptr_t>(stack);
      if (_state.exchange(state, std::memory_order_acq_rel) == ready)
      {
        Scheduler::enable(stack);
      }
    }

    T await_resume() noexcept
    {
      return std::move(_value);
    }
  };


  template <typename T>
  struct Promise<T&>
  {
    static constexpr std::uintptr_t ready {0};
    static constexpr std::uintptr_t no_waiter {1};

    std::atomic_uintptr_t _state {no_waiter};
    T* _value;

    void put(T& value)
    {
      _value = std::addressof(value);
      auto state = _state.exchange(ready, std::memory_order_acq_rel);
      if (state != no_waiter)
      {
        Scheduler::enable(reinterpret_cast<Stack *>(state));
      }
    }

    bool await_ready() noexcept
    {
      return _state.load(std::memory_order_acquire) == ready;
    }

    void await_suspend(std::coroutine_handle<> coroutine) noexcept
    {
      auto stack = Scheduler::suspend(coroutine);
      auto state = reinterpret_cast<std::uintptr_t>(stack);
      if (_state.exchange(state, std::memory_order_acq_rel) == ready)
      {
        Scheduler::enable(stack);
      }
    }

    T& await_resume() noexcept
    {
      return *_value;
    }
  };


  template <>
  struct Promise<void>
  {
    static constexpr std::uintptr_t ready {0};
    static constexpr std::uintptr_t no_waiter {1};

    std::atomic_uintptr_t _state {no_waiter};

    void put()
    {
      auto state = _state.exchange(ready, std::memory_order_acq_rel);
      if (state != no_waiter)
      {
        Scheduler::enable(reinterpret_cast<Stack *>(state));
      }
    }

    bool await_ready() noexcept
    {
      return _state.load(std::memory_order_acquire) == ready;
    }

    void await_suspend(std::coroutine_handle<> coroutine) noexcept
    {
      auto stack = Scheduler::suspend(coroutine);
      auto state = reinterpret_cast<std::uintptr_t>(stack);
      if (_state.exchange(state, std::memory_order_acq_rel) == ready)
      {
        Scheduler::enable(stack);
      }
    }

    void await_resume() noexcept {}
  };

}


#endif // TYPON_PROMISE_HPP_INCLUDED
