#ifndef TYPON_RESULT_HPP_INCLUDED
#define TYPON_RESULT_HPP_INCLUDED


#include <exception>
#include <memory>
#include <type_traits>
#include <utility>


namespace typon
{

  template <typename T, typename E = std::exception_ptr>
  struct Result
  {
    using value_type = T;

    bool _valid = false;
    [[no_unique_address]] E _exception;
    union
    {
      T _value;
    };

    Result() noexcept {}

    ~Result()
    {
      if (_valid)
      {
        std::destroy_at(std::addressof(_value));
      }
    }

    template <typename U>
    void return_value(U&& expr) noexcept(std::is_nothrow_constructible_v<T, U&&>)
    {
      std::construct_at(std::addressof(_value), std::forward<U>(expr));
      _valid = true;
    }

    void return_value(T&& expr) noexcept
    {
      return_value<T>(std::move(expr));
    }

    void unhandled_exception() noexcept
    {
      if constexpr(std::is_assignable_v<E, std::exception_ptr>)
      {
        _exception = std::current_exception();
      }
    }

    T& get() &
    {
      if constexpr(std::is_same_v<E, std::exception_ptr>)
      {
        if (_exception)
        {
          std::rethrow_exception(std::exchange(_exception, nullptr));
        }
      }
      return _value;
    }

    T&& get() &&
    {
      if constexpr(std::is_same_v<E, std::exception_ptr>)
      {
        if (_exception)
        {
          std::rethrow_exception(std::exchange(_exception, nullptr));
        }
      }
      return std::move(_value);
    }

    T& value() & noexcept
    {
      return _value;
    }

    T&& value() && noexcept
    {
      return std::move(_value);
    }

  };


  template <typename T, typename E>
  struct Result<T&, E>
  {
    using value_type = T&;

    T* _value;
    [[no_unique_address]] E _exception;

    void return_value(T& expr) noexcept
    {
      _value = std::addressof(expr);
    }

    void unhandled_exception() noexcept
    {
      if constexpr(std::is_assignable_v<E, std::exception_ptr>)
      {
        _exception = std::current_exception();
      }
    }

    T& get() &
    {
      if constexpr(std::is_same_v<E, std::exception_ptr>)
      {
        if (_exception)
        {
          std::rethrow_exception(std::exchange(_exception, nullptr));
        }
      }
      return *_value;
    }

    T& value() & noexcept
    {
      return *_value;
    }
  };


  template <typename E>
  struct Result<void, E>
  {
    using value_type = void;

    [[no_unique_address]] E _exception;

    void return_void() noexcept {}

    void unhandled_exception() noexcept
    {
      if constexpr(std::is_assignable_v<E, std::exception_ptr>)
      {
        _exception = std::current_exception();
      }
    }

    void get()
    {
      if constexpr(std::is_same_v<E, std::exception_ptr>)
      {
        if (_exception)
        {
          std::rethrow_exception(std::exchange(_exception, nullptr));
        }
      }
    }

    void value() noexcept {}
  };

}

#endif // TYPON_RESULT_HPP_INCLUDED
