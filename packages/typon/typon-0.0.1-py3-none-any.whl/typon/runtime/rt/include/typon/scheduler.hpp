#ifndef TYPON_SCHEDULER_HPP_INCLUDED
#define TYPON_SCHEDULER_HPP_INCLUDED

/* Continuation-stealing scheduler */

/* Papers:

   .  N. S. Arora, R. D. Blumofe, and C. G. Plaxton. 1998.
      Thread scheduling for multiprogrammed multiprocessors.
      https://doi.org/10.1145/277651.277678

   .  C. X. Lin, T .W Huang, and M. D. F. Wong. 2020.
      An efficient work-stealing scheduler for task dependency graph.
      https://tsung-wei-huang.github.io/papers/icpads20.pdf

   .  F. Schmaus, N. Pfeiffer, W. Schröder-Preikschat, T. Hönig, and J. Nolte.
      2021. Nowa: a wait-free continuation-stealing concurrency platform.
      https://www4.cs.fau.de/Publications/2021/schmaus2021nowa.pdf
*/


#include <atomic>
#include <bit>
#include <coroutine>
#include <cstdint>
#include <exception>
#include <thread>
#include <utility>
#include <vector>

#include <typon/event_count.hpp>
#include <typon/garbage_collector.hpp>
#include <typon/pool.hpp>
#include <typon/random.hpp>
#include <typon/stack.hpp>
#include <typon/syscall_completion.hpp>
#include <typon/theft_point.hpp>

#include <liburing.h>

namespace typon
{


  struct Scheduler
  {
    using uint = unsigned int;
    using u64 = std::uint_fast64_t;

    std::atomic_bool _done {false};
    const uint _concurrency;
    const uint _mask;
    std::atomic<uint> _thieves = 0;
    std::atomic<u64> _potential = 0;
    EventCount<> _notifyer;
    std::vector<Pool> _pool;
    std::vector<Stack *> _stack;
    std::vector<io_uring> _ring;
    std::vector<std::thread> _thread;
    std::vector<std::thread> _io_thread;
    GarbageCollector _gc;

    static inline thread_local uint thread_id;

    static Scheduler & get() noexcept
    {
      static Scheduler scheduler {std::thread::hardware_concurrency()};
      return scheduler;
    }

    static io_uring * ring() noexcept
    {
      return &(get()._ring[thread_id]);
    }

    static void schedule(std::coroutine_handle<> coroutine) noexcept
    {
      Pool & pool = get().random();
      Stack * stack = new Stack(Stack::READY);
      {
        auto lock_guard = pool.lock_guard();
        pool.add(stack);
      }
      stack->_coroutine = coroutine;
      get()._potential.fetch_add(1);
      get()._notifyer.notify_one();
    }

    static void push(TheftPoint * task) noexcept
    {
      get()._stack[thread_id]->push(task);
    }

    static bool pop() noexcept
    {
      bool result = get()._stack[thread_id]->pop();
      if (auto garbage = get()._stack[thread_id]->reclaim())
      {
        get()._gc.retire(garbage);
      }
      return result;
    }

    static TheftPoint * peek() noexcept
    {
      return get()._stack[thread_id]->peek();
    }

    static auto suspend(std::coroutine_handle<> coroutine) noexcept
    {
      Stack * stack = std::exchange(get()._stack[thread_id], nullptr);
      stack->_coroutine = coroutine;
      stack->_state.store(Stack::WAITING);
      return stack;
    }

    static void enable(Stack * stack) noexcept
    {
      auto state = stack->_state.exchange(Stack::READY);
      if (state == Stack::EMPTY)
      {
        Pool & pool = get().random();
        {
          auto lock_guard = pool.lock_guard();
          pool.add(stack);
        }
        get()._potential.fetch_add(1);
        get()._notifyer.notify_one();
      }
    }

    Scheduler(uint concurrency) noexcept
      : _concurrency(concurrency)
      , _mask((1 << std::bit_width(concurrency)) - 1)
      , _pool(this->_mask + 1)
      , _stack(concurrency, nullptr)
      , _ring(concurrency)
      , _gc(concurrency)
    {
      // Initialize I/O rings
      for (uint id = 0; id < concurrency; id++)
      {
        // The queue depth can be 1 because we submit requests one by one
        if (io_uring_queue_init(1, &(_ring[id]), 0))
        {
          std::terminate();
        }
      }

      // Spawn worker threads
      for (uint id = 0; id < concurrency; id++)
      {
        _thread.emplace_back([this, id]() {
          thread_id = id;
          for(;;)
          {
            std::coroutine_handle<> coroutine;
            if (!wait_for_work(coroutine))
            {
              break;
            }
            coroutine.resume();
          }
        });
      }

      // Spawn I/O completion threads
      for (uint id = 0; id < concurrency; id++)
      {
        _io_thread.emplace_back([this, id]() {
          io_uring * ring = &(_ring[id]);
          for(;;)
          {
            io_uring_cqe * cqe;
            if (io_uring_wait_cqe(ring, &cqe))
            {
              throw std::runtime_error("io_uring_wait_cqe() failed");
            }
            void * data = io_uring_cqe_get_data(cqe);
            auto result = cqe->res;
            io_uring_cqe_seen(ring, cqe);
            if (!data)
            {
              break;
            }
            auto completion = reinterpret_cast<SyscallCompletion *>(data);
            completion->_result = result;
            Scheduler::enable(completion->_stack);
          }
        });
      }
    }

    bool wait_for_work(std::coroutine_handle<> & coroutine) noexcept
    {
      for(;;)
      {
        _thieves.fetch_add(1);
        find_work(coroutine);
        if (coroutine)
        {
          prepare_stack();
          if (_thieves.fetch_sub(1) == 1)
          {
            _notifyer.notify_one();
          }
          return true;
        }
        auto key = _notifyer.prepare_wait();
        if (_done.load())
        {
          _notifyer.cancel_wait();
          _notifyer.notify_all();
          _thieves.fetch_sub(1);
          return false;
        }
        if (_thieves.fetch_sub(1) == 1)
        {
          if (_potential.load() > 0)
          {
            _notifyer.cancel_wait();
            continue;
          }
        }
        _notifyer.wait(key);
      }
    }

    void find_work(std::coroutine_handle<> & coroutine) noexcept
    {
      auto epoch = _gc.epoch(thread_id);
      for (uint i = 0; i < _concurrency * 2 + 1; i++)
      {
        Pool & pool = random();
        if (!pool.try_lock())
        {
          continue;
        }
        auto lock_guard = pool.adopt_lock_guard();
        auto size = pool.size();
        if (!size)
        {
          continue;
        }
        auto index = size > 1 ? random::random() % size : 0;
        auto stack = pool.get(index);
        auto state = stack->_state.load();
        if (state == Stack::ACTIVE)
        {
          if (auto task = stack->steal())
          {
            coroutine = task;
          }
          return;
        }
        if (state == Stack::WAITING)
        {
          if (auto task = stack->pop_top())
          {
            coroutine = task;
            return;
          }
          if (stack->_state.compare_exchange_strong(state, Stack::EMPTY))
          {
            _potential.fetch_sub(1);
            pool.remove(index);
            return;
          }
          adopt_stack(stack);
          coroutine = stack->_coroutine;
          return;
        }
        if (state == Stack::READY)
        {
          adopt_stack(stack);
          coroutine = stack->_coroutine;
          return;
        }
        if (state == Stack::DONE)
        {
          pool.remove(index);
          delete stack;
          return;
        }
      }
    }

    void adopt_stack(Stack * stack) noexcept
    {
      stack->_state.store(Stack::ACTIVE);
      if (auto old = std::exchange(_stack[thread_id], stack))
      {
        _potential.fetch_sub(1);
        old->_state.store(Stack::DONE);
      }
    }

    void prepare_stack() noexcept
    {
      if (!_stack[thread_id])
      {
        auto stack = _stack[thread_id] = new Stack(Stack::ACTIVE);
        Pool & pool = random();
        {
          auto lock_guard = pool.lock_guard();
          pool.add(stack);
        }
        _potential.fetch_add(1);
        _notifyer.notify_one();
      }
    }

    Pool & random() noexcept
    {
      return _pool[random::random() & _mask];
    }

    ~Scheduler() noexcept
    {
      // Signal worker threads to stop
      _done.store(true);
      _notifyer.notify_all();
      // Wait until all worker threads are done
      for (auto & t : _thread)
      {
        t.join();
      }
      // Signal I/O threads to stop
      for (uint id = 0; id < _concurrency; id++)
      {
        // An sqe should be available, because SQPOLL is not used
        io_uring_sqe * sqe = io_uring_get_sqe(&(_ring[id]));
        io_uring_prep_nop(sqe);
        io_uring_sqe_set_data(sqe, nullptr);
        io_uring_submit(&(_ring[id]));
      }
      // Wait until all I/O threads are done
      for (auto & t : _io_thread)
      {
        t.join();
      }
      // Cleanup all I/O rings
      for (uint id = 0; id < _concurrency; id++)
      {
        io_uring_queue_exit(&(_ring[id]));
      }
    }
  };

}

#endif // TYPON_SCHEDULER_HPP_INCLUDED
