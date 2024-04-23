#ifndef TYPON_EVENT_COUNT_HPP_INCLUDED
#define TYPON_EVENT_COUNT_HPP_INCLUDED

#include <atomic>
#include <cstdint>


namespace typon
{

  template <unsigned int N = 10>
  struct EventCount
  {
    using u64 = std::uint_fast64_t;

    static_assert(N < 16);

    static constexpr u64 shift = u64(1) << N;
    static constexpr u64 mask = shift - 1;

    std::atomic<u64> _state {0};

    auto prepare_wait() noexcept
    {
      return _state.load(std::memory_order_acquire);
    }

    void cancel_wait() noexcept {}

    void wait(u64 key) noexcept
    {
      u64 state = _state.fetch_add(1, std::memory_order_acq_rel) + 1;
      for(;;)
      {
        if ((state ^ key) & (~mask))
        {
          break;
        }
        key = state;
        _state.wait(key, std::memory_order_acquire);
        state = _state.load(std::memory_order_acquire);
      }
      _state.fetch_sub(1, std::memory_order_seq_cst);
    }

    void notify_one() noexcept
    {
      if (_state.fetch_add(shift, std::memory_order_acq_rel) & mask)
      {
        _state.notify_one();
      }
    }

    void notify_all() noexcept
    {
      if (_state.fetch_add(shift, std::memory_order_acq_rel) & mask)
      {
        _state.notify_all();
      }
    }
  };

}


#endif // TYPON_EVENT_COUNT_HPP_INCLUDED
