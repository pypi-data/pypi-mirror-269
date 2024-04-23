#ifndef TYPON_SPAN_HPP_INCLUDED
#define TYPON_SPAN_HPP_INCLUDED

#include <atomic>
#include <concepts>
#include <coroutine>
#include <cstdint>
#include <exception>
#include <limits>
#include <vector>

#include <typon/defer.hpp>
#include <typon/theft_point.hpp>


namespace typon
{

  struct Span : TheftPoint
  {
    using u64 = std::uint_fast64_t;

    static constexpr u64 UMAX = std::numeric_limits<u64>::max();

    std::coroutine_handle<> _coroutine;
    std::coroutine_handle<> _continuation;

    u64 _thefts = 0;

    std::atomic<bool> _concurrent_error_flag { false };
    std::exception_ptr _concurrent_exception;
    std::exception_ptr _sequential_exception;

    std::atomic<u64> _n = UMAX;

    Span(std::coroutine_handle<> coroutine) noexcept
      : _coroutine(coroutine)
    {}

    void propagate_exception()
    {
      if (_sequential_exception)
      {
        std::rethrow_exception(_sequential_exception);
      }
      if (_concurrent_exception)
      {
        std::rethrow_exception(_concurrent_exception);
      }
    }

    bool has_concurrent_exception() noexcept
    {
      return _concurrent_error_flag.load(std::memory_order_acquire);
    }

    void set_concurrent_exception(std::exception_ptr & exception) noexcept
    {
      if (!_concurrent_error_flag.exchange(true, std::memory_order_acq_rel))
      {
        _concurrent_exception = exception;
      }
    }

    void set_sequential_exception(std::exception_ptr exception) noexcept
    {
      _sequential_exception = std::move(exception);
    }

    bool notify_sync() noexcept
    {
      u64 n = _n.fetch_sub(UMAX - _thefts, std::memory_order_acq_rel);
      return (n - (UMAX - _thefts) == 0);
    }

    bool notify_fork() noexcept
    {
      u64 n = _n.fetch_sub(1, std::memory_order_acq_rel);
      return (n == 1);
    }

    void reset_sync() noexcept
    {
      _thefts = 0;
      _n.store(UMAX, std::memory_order_release);
    }

    std::coroutine_handle<> steal() noexcept override
    {
      _thefts++;
      return _coroutine;
    }

    operator std::coroutine_handle<>() noexcept
    {
      return _coroutine;
    }

    std::coroutine_handle<> fork_continuation() noexcept
    {
      // It's safe to access _concurrent_exception here
      // because this is only called when all strands are done
      if (_coroutine.done() || _sequential_exception || _concurrent_exception)
      {
        return _continuation;
      }
      return _coroutine;
    }

    std::coroutine_handle<> sync_continuation() noexcept
    {
      // It's safe to access _concurrent_exception here
      // because this is only called when all strands are done
      if (_sequential_exception || _concurrent_exception)
      {
        return _continuation;
      }
      return _coroutine;
    }
  };

}


#endif // TYPON_SPAN_HPP_INCLUDED
