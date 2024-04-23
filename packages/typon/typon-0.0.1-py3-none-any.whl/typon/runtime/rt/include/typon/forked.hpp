#ifndef TYPON_FORKED_HPP_INCLUDED
#define TYPON_FORKED_HPP_INCLUDED

#include <coroutine>
#include <memory>
#include <type_traits>
#include <utility>

#include <typon/defer.hpp>
#include <typon/fork_refcount.hpp>
#include <typon/result.hpp>


namespace typon
{

  template <typename T>
  struct Forked
  {
    using value_type = T;

    Result<T> * _result = nullptr;
    union
    {
      T _value;
      ForkRefcount * _refcount;
    };

    template <typename Promise>
    Forked(std::coroutine_handle<Promise> coroutine, bool ready)
    {
      if (ready)
      {
        std::construct_at(std::addressof(_value), coroutine.promise().value());
        coroutine.destroy();
      }
      else
      {
        _refcount = &(coroutine.promise()._refcount);
        _result = &(coroutine.promise());
      }
    }

    Forked(Forked && other) noexcept(std::is_nothrow_move_constructible_v<T>)
    {
      _result = other._result;
      if (_result)
      {
        _refcount = std::exchange(other._refcount, nullptr);
      }
      else
      {
        std::construct_at(std::addressof(_value), std::move(other._value));
      }
    }

    Forked(const Forked &) = delete;
    Forked& operator=(const Forked &) = delete;

    Forked& operator=(Forked && other)
      noexcept(std::is_nothrow_move_constructible_v<T>)
    {
      if (this != &other)
      {
        Forked old { std::move(*this) };
        _result = other._result;
        if (_result)
        {
          _refcount = std::exchange(other._refcount, nullptr);
        }
        else
        {
          std::construct_at(std::addressof(_value), std::move(other._value));
        }
      }
      return *this;
    }

    ~Forked()
    {
      if (_result)
      {
        if (_refcount) {
            _refcount->decref();
        }
      }
      else
      {
        std::destroy_at(std::addressof(_value));
      }
    }

    T get() &
    {
      if (_result)
      {
        return _result->value();
      }
      return _value;
    }

    T get() &&
    {
      if (_result)
      {
        return _result->value();
      }
      return std::move(_value);
    }

    auto operator->() &
    {
      return this;
    }
  };


  template <typename T>
  struct Forked<T&>
  {
    using value_type = T;

    Result<T> * _result = nullptr;
    void * _data;

    template <typename Promise>
    Forked(std::coroutine_handle<Promise> coroutine, bool ready)
    {
      if (ready)
      {
        _data = std::addressof(coroutine.promise().value());
        coroutine.destroy();
      }
      else
      {
        _data = &(coroutine.promise()._refcount);
        _result = &(coroutine.promise());
      }
    }

    Forked(const Forked &) = delete;
    Forked& operator=(const Forked &) = delete;

    Forked(Forked && other) noexcept(std::is_nothrow_move_constructible_v<T>)
    {
      _result = other._result;
      _data = std::exchange(other._data, nullptr);
    }

    Forked& operator=(Forked other)
      noexcept(std::is_nothrow_move_constructible_v<T>)
    {
      std::swap(_result, other._result);
      std::swap(_data, other._data);
      return *this;
    }

    ~Forked()
    {
      if (_result)
      {
        if (_data) {
            reinterpret_cast<ForkRefcount *>(_data)->decref();
        }
      }
    }

    T& get()
    {
      if (_result)
      {
        return _result->value();
      }
      return *(reinterpret_cast<T *>(_data));
    }

    auto operator->() &
    {
      return this;
    }
  };


  template <typename T>
    requires requires { sizeof(T); } && (sizeof(T) > 2 * sizeof(void*))
  struct Forked<T>
  {
    using value_type = T;

    bool _ready;
    Result<T> * _result;
    void * _coroutine;

    template <typename Promise>
    Forked(std::coroutine_handle<Promise> coroutine, bool ready)
    {
      _ready = ready;
      _result = &(coroutine.promise());
      if (ready)
      {
        _coroutine = coroutine.address();
        coroutine.promise().get();
      }
      else
      {
        _coroutine = &(coroutine.promise()._refcount);
      }
    }

    Forked(const Forked &) = delete;
    Forked& operator=(const Forked &) = delete;

    Forked(Forked && other) noexcept
      : _ready(other._ready)
      , _result(other._result)
      , _coroutine(std::exchange(other._coroutine, nullptr))
    {}

    Forked& operator=(Forked && other) noexcept
    {
      std::swap(_ready, other._ready);
      std::swap(_result, other._result);
      std::swap(_coroutine, other._coroutine);
      return *this;
    }

    ~Forked()
    {
      if (_coroutine)
      {
        if (_ready)
        {
          std::coroutine_handle<void>::from_address(_coroutine).destroy();
        }
        else
        {
          reinterpret_cast<ForkRefcount *>(_coroutine)->decref();
        }
      }
    }

    T get()
    {
      return _result->value();
    }

    auto operator->() &
    {
      return this;
    }
  };

}


#endif // TYPON_FORKED_HPP_INCLUDED
