#ifndef TYPON_FUNDAMENTAL_STACK_HPP_INCLUDED
#define TYPON_FUNDAMENTAL_STACK_HPP_INCLUDED

/* Work-stealing deque */

/* A stack of continuations that may be stolen and resumed concurrently.
   Continuations are pushed when a potentially concurrent child task is
   started and popped when the child completes, unless stolen first by a
   concurrent worker. Thieves steal from the oldest continuations first,
   while completed children tasks try to resume the most recent.

   Furthermore, the whole stack may be suspended while waiting for an
   asynchronous operation. In that case thieves may still steal but the
   most recent child task is suspended. Suspended stacks will be enabled
   when the asynchronous operation completes, at which point a thief may
   take over the whole stack and resume the suspended child task.

   There are five possible states:
   - ACTIVE: A worker is actively running a child task.
   - WAITING: Waiting on an asynchronous operation.
   - EMPTY: Like WAITING, but no continuation remains unstolen.
   - READY: A thief may take the whole stack and resume the suspended task.
   - DONE: No more task remains, suspended or otherwise.

   Papers:

   .  D. Chase and Y. Lev. 2005.
      Dynamic circular work-stealing deque.
      https://doi.org/10.1145/1073970.1073974

   .  N. M. Lê, A. Pop, A. Cohen, and F. Zappa Nardelli. 2013.
      Correct and efficient work-stealing for weak memory models.
      https://doi.org/10.1145/2517327.2442524

   .  Kyle Singer, Yifan Xu, and I-Ting Angelina Lee. 2019.
      Proactive work stealing for futures.
      https://doi.org/10.1145/3293883.3295735
*/


#include <atomic>
#include <coroutine>
#include <cstdint>
#include <memory>
#include <type_traits>
#include <utility>

#include <typon/ring_buffer.hpp>
#include <typon/theft_point.hpp>


namespace typon
{

  struct Stack
  {
    using RingBuffer = typon::RingBuffer<TheftPoint *>;
    using u64 = RingBuffer::u64;

    using enum std::memory_order;

    enum State : unsigned char { ACTIVE, WAITING, EMPTY, READY, DONE };

    std::atomic<u64> _top {1};
    std::atomic<u64> _bottom {1};
    std::atomic<RingBuffer *> _buffer;
    std::atomic<State> _state;
    std::coroutine_handle<> _coroutine;

    Stack(State state) noexcept
      : _buffer(new RingBuffer(3))
      , _state(state)
    {}

    ~Stack()
    {
      delete _buffer.load(relaxed);
    }

    void push(TheftPoint * x) noexcept
    {
      u64 bottom = _bottom.load(relaxed);
      u64 top = _top.load(acquire);
      RingBuffer * buffer = _buffer.load(relaxed);
      if (bottom - top > buffer->capacity() - 1)
      {
        buffer = buffer->grow(top, bottom);
        _buffer.store(buffer);
      }
      buffer->put(bottom, x);
      std::atomic_thread_fence(release);
      _bottom.store(bottom + 1, relaxed);
    }

    bool pop() noexcept
    {
      u64 bottom = _bottom.load(relaxed) - 1;
      _bottom.store(bottom, relaxed);
      std::atomic_thread_fence(seq_cst);
      u64 top = _top.load(relaxed);
      if (top < bottom)
      {
        return true;
      }
      if (top == bottom)
      {
        bool win = _top.compare_exchange_strong(top, top + 1, seq_cst, relaxed);
        _bottom.store(bottom + 1, relaxed);
        return win;
      }
      _bottom.store(bottom + 1, relaxed);
      return false;
    }

    TheftPoint * peek() noexcept
    {
      u64 bottom = _bottom.load(relaxed) - 1;
      RingBuffer * buffer = _buffer.load(relaxed);
      return buffer->get(bottom);
    }

    std::coroutine_handle<> steal() noexcept
    {
      u64 top = _top.load(acquire);
      std::atomic_thread_fence(seq_cst);
      u64 bottom = _bottom.load(acquire);
      RingBuffer * buffer = _buffer.load(consume);
      if (top < bottom)
      {
        TheftPoint * x = buffer->get(top);
        if (!_top.compare_exchange_strong(top, top + 1, seq_cst, relaxed))
        {
          return nullptr;
        }
        return x->steal();
      }
      return nullptr;
    }

    std::coroutine_handle<> pop_top() noexcept
    {
      u64 top = _top.load(relaxed);
      u64 bottom = _bottom.load(relaxed);
      auto buffer = _buffer.load(relaxed);
      if (top < bottom)
      {
        TheftPoint * x = buffer->get(top);
        _top.store(top + 1, relaxed);
        if (auto garbage = reclaim())
        {
          delete garbage;
        }
        return x->steal();
      }
      if (auto garbage = reclaim())
      {
        delete garbage;
      }
      return nullptr;
    }

    RingBuffer * reclaim() noexcept
    {
      u64 bottom = _bottom.load(relaxed);
      u64 top = _top.load(relaxed);
      auto buffer = _buffer.load(relaxed);
      u64 capacity = buffer->capacity();
      if (bottom < top + (capacity >> 2))
      {
        if (auto next = buffer->shrink(top, bottom))
        {
          _buffer.store(next, relaxed);
          return buffer;
        }
      }
      return nullptr;
    }
  };

}


#endif // TYPON_FUNDAMENTAL_STACK_HPP_INCLUDED
