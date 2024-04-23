#ifndef TYPON_POOL_HPP_INCLUDED
#define TYPON_POOL_HPP_INCLUDED

#include <mutex>
#include <vector>

#include <typon/stack.hpp>


namespace typon
{

  struct Pool
  {
    using Vector = std::vector<Stack *>;
    using Size = Vector::size_type;

    std::mutex _mutex;
    Vector _pool;

    auto lock_guard() noexcept
    {
      return std::lock_guard(_mutex);
    }

    auto adopt_lock_guard() noexcept
    {
      return std::lock_guard(_mutex, std::adopt_lock);
    }

    bool try_lock() noexcept
    {
      return _mutex.try_lock();
    }

    void add(Stack * stack) noexcept
    {
      _pool.push_back(stack);
    }

    auto size() noexcept
    {
      return _pool.size();
    }

    Stack * get(Size index) noexcept
    {
      return _pool[index];
    }

    void remove(Size index) noexcept
    {
      _pool[index] = _pool.back();
      _pool.pop_back();
    }

    ~Pool()
    {
      for (auto & stack : _pool)
      {
        delete stack;
      }
    }
  };

}


#endif // TYPON_POOL_HPP_INCLUDED
