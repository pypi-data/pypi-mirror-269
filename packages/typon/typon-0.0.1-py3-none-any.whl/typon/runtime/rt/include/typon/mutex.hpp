#ifndef TYPON_MUTEX_HPP_INCLUDED
#define TYPON_MUTEX_HPP_INCLUDED

#include <atomic>
#include <coroutine>
#include <cstdint>

#include <typon/scheduler.hpp>
#include <typon/stack.hpp>


namespace typon
{

  /* An asynchronous mutex.

     Inspired by the implementation in CppCoro by Lewis Baker.
     https://github.com/lewissbaker/cppcoro
  */
  struct Mutex
  {
    struct Node
    {
      Node * _next;
      std::atomic<std::uintptr_t> _stack { 0 };
    };

    using enum std::memory_order;

    std::atomic<Node *> _state { nullptr };
    Node * _waiters { nullptr };

    [[nodiscard]] auto lock() noexcept
    {
      struct awaitable : Node
      {
        Mutex * _mutex;

        bool await_ready() noexcept
        {
          std::atomic<Node *> & state = _mutex->_state;
          Node * next = nullptr;
          for(;;)
          {
            // _next must be properly set before updating _state
            _next = next;
            if(state.compare_exchange_weak(next, this, acq_rel, relaxed))
            {
              return !next;
            }
          }
        }

        void await_suspend(std::coroutine_handle<> coroutine) noexcept
        {
          auto stack = Scheduler::suspend(coroutine);
          if (_stack.exchange(reinterpret_cast<std::uintptr_t>(stack)))
          {
            Scheduler::enable(stack);
          }
        }

        void await_resume() noexcept {};

        ~awaitable()
        {
          Node * waiter = _mutex->_waiters;
          if (!waiter)
          {
            Node * next = this;
            if (_mutex->_state.compare_exchange_strong(next, nullptr, acq_rel))
            {
              return;
            }
            while (next != this)
            {
              auto tmp = next->_next;
              next->_next = waiter;
              waiter = next;
              next = tmp;
            }
          }
          _mutex->_waiters = waiter->_next;
          auto stack = waiter->_stack.exchange(1);
          if (stack)
          {
            Scheduler::enable(reinterpret_cast<Stack *>(stack));
          }
        }
      };

      return awaitable { {}, this };
    }
  };

}


#endif // TYPON_MUTEX_HPP_INCLUDED
