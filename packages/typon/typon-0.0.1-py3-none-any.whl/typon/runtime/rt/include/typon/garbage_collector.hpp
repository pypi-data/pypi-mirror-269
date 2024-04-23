#ifndef TYPON_GARBAGE_COLLECTOR_HPP_INCLUDED
#define TYPON_GARBAGE_COLLECTOR_HPP_INCLUDED

#include <atomic>
#include <bit>
#include <cstdint>
#include <type_traits>


namespace typon
{

  struct GarbageCollector
  {
    using u64 = std::uint_fast64_t;
    using uint = unsigned int;

    using enum std::memory_order;

    struct node
    {
      const u64 _stamp;
      std::atomic<node *> _next {nullptr};

      node(u64 stamp) noexcept : _stamp(stamp) {};

      virtual ~node() {}
    };

    template <typename T>
    struct garbage : node
    {
      T * _ptr;

      garbage(T * ptr, u64 stamp) noexcept
        : node(stamp)
        , _ptr(ptr)
      {}

      virtual ~garbage()
      {
        delete _ptr;
      }
    };

    const uint _concurrency;
    const uint _bits;
    std::atomic<u64> * const _stamps;
    std::atomic<u64> _state {0};
    std::atomic<node *> _head;
    std::atomic<node *> _tail;

    GarbageCollector(uint concurrency) noexcept
      : _concurrency(concurrency)
      , _bits(std::bit_width(concurrency))
      , _stamps(new std::atomic<u64>[concurrency])
    {
      auto first = new node(0);
      _head.store(first);
      _tail.store(first);
      for (uint i = 0; i < _concurrency; i++)
      {
        _stamps[i].store(u64(-1));
      }
    }

    auto epoch(uint id) noexcept
    {
      struct Epoch
      {
        GarbageCollector & _gc;
        uint _id;

        ~Epoch()
        {
          _gc.leave(_id);
        }
      };

      enter(id);
      return Epoch { *this, id };
    }

    void enter(uint id) noexcept
    {
      auto state = _state.fetch_add((1 << _bits) + 1);
      _stamps[id].store(state >> _bits);
    }

    template <typename T>
    void retire(T * ptr) noexcept
    {
      auto state = _state.load();
      if ((state & ((1 << _bits) - 1)) == 0)
      {
        delete ptr;
      }
      else
      {
        auto node = new garbage<T> { ptr, state >> _bits };
        auto head = _head.exchange(node);
        head->_next.store(node);
      }
    }

    void leave(uint id) noexcept
    {
      _state.fetch_sub(1);
      _stamps[id].store(u64(-1));
      if (_tail.load())
      {
        reclaim(oldest());
      }
    }

    u64 oldest() noexcept
    {
      u64 oldest = u64(-1);
      for (uint i = 0; i < _concurrency; i++)
      {
        u64 stamp = _stamps[i].load(relaxed);
        if (stamp < oldest)
        {
          oldest = stamp;
        }
      }
      return oldest;
    }

    void reclaim(u64 oldest) noexcept
    {
      auto tail = _tail.load();
      while (true)
      {
        if (tail->_stamp >= oldest)
        {
          break;
        }
        auto next = tail->_next.load();
        if (!next)
        {
          break;
        }
        if (_tail.compare_exchange_strong(tail, next))
        {
          delete tail;
          tail = next;
        }
      }
    }

    ~GarbageCollector()
    {
      delete[] _stamps;
      auto tail = _tail.load();
      while (tail)
      {
        auto next = tail->_next.load();
        delete tail;
        tail = next;
      }
    }
  };
}


#endif // TYPON_GARBAGE_COLLECTOR_HPP_INCLUDED
