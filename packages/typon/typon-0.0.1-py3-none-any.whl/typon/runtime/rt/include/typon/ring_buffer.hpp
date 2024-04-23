#ifndef TYPON_RING_BUFFER_HPP_INCLUDED
#define TYPON_RING_BUFFER_HPP_INCLUDED

#include <atomic>
#include <bit>
#include <cstdint>
#include <type_traits>

#include <typon/ring.hpp>


namespace typon
{

  template <typename T>
    requires std::is_trivially_copyable_v<T>
    && std::is_trivially_destructible_v<T>
  struct RingBuffer
  {
    using u8 = std::uint_least8_t;
    using u64 = std::uint_fast64_t;

    using enum std::memory_order;

    Ring<u64> _ring;
    RingBuffer * _next;
    std::atomic<T> * const _array;

    RingBuffer(u8 bits, RingBuffer * next = nullptr) noexcept
      : _ring(bits)
      , _next(next)
      , _array(new std::atomic<T>[this->capacity()])
    {}

    ~RingBuffer()
    {
      delete [] _array;
      if (_next)
      {
        delete _next;
      }
    }

    u64 capacity() noexcept
    {
      return _ring.size();
    }

    void put(u64 index, T object) noexcept
    {
      _array[index % _ring].store(std::move(object), relaxed);
    }

    T get(u64 index) noexcept
    {
      return _array[index % _ring].load(relaxed);
    }

    RingBuffer * fill(RingBuffer * sink, u64 start, u64 end) noexcept
    {
      for (u64 i = start; i < end; i++)
      {
        sink->put(i, get(i));
      }
      return sink;
    }

    RingBuffer * grow(u64 start, u64 end) noexcept
    {
      auto buffer = new RingBuffer(std::countr_zero(_ring.size()) + 1, this);
      return fill(buffer, start, end);
    }

    RingBuffer * shrink(u64 start, u64 end) noexcept
    {
      RingBuffer * last = nullptr;
      auto next = this;
      auto size = (end - start);
      auto threshold = size * 2;
      while (next->_next && next->_next->capacity() >= threshold)
      {
        last = next;
        next = next->_next;
      }
      if (!last)
      {
        return nullptr;
      }
      return fill(std::exchange(last->_next, nullptr), start, end);

    }
  };

}


#endif //  TYPON_RING_BUFFER_HPP_INCLUDED
