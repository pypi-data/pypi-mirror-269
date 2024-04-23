#ifndef TYPON_FORK_REFCOUNT_HPP_INCLUDED
#define TYPON_FORK_REFCOUNT_HPP_INCLUDED

#include <atomic>
#include <coroutine>


namespace typon
{

  struct ForkRefcount
  {
    std::coroutine_handle<> _coroutine;
    std::atomic<bool> _refcount {true};

    void set(std::coroutine_handle<> coroutine) noexcept
    {
      _coroutine = coroutine;
    }

    void decref() noexcept
    {
      if (!_refcount.exchange(false, std::memory_order_acq_rel))
      {
        _coroutine.destroy();
      }
    }
  };

}


#endif // TYPON_FORK_REFCOUNT_HPP_INCLUDED
