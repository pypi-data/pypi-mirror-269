//
// Created by Tom on 13/03/2023.
//

#ifndef TYPON_GENERATOR_HPP
#define TYPON_GENERATOR_HPP

#include <coroutine>

namespace typon {

/**
 * https://github.com/feabhas/coroutines-blog
 */
template <typename T> class Generator {

public:
  using value_type = T;
  class promise_type;

  explicit Generator(std::coroutine_handle<promise_type> coroutine) noexcept
      : _coroutine(coroutine) {}

  Generator(const Generator &) = delete;
  Generator &operator=(const Generator &) = delete;

  Generator(Generator &&other) noexcept
      : _coroutine(std::exchange(other._coroutine, nullptr)) {}

  Generator &operator=(Generator other) {
    std::swap(_coroutine, other._coroutine);
    return *this;
  }

  ~Generator() {
    if (_coroutine) {
      _coroutine.destroy();
    }
  }

  Task<Generator> async_self() {
    co_return std::move(*this);
  }

  auto operator co_await() && noexcept {
    return std::move(async_self().operator co_await());
  }

  class promise_type {
  public:
    using value_type = std::optional<T>;

    promise_type() = default;
    std::suspend_always initial_suspend() { return {}; }
    std::suspend_always final_suspend() noexcept {
      final = true;
      return {};
    }
    void unhandled_exception() {
      std::rethrow_exception(std::move(std::current_exception()));
    }

    std::suspend_always yield_value(T value) {
      this->value = std::move(value);
      return {};
    }

    // void return_value(T value) {
    //     this->value = std::move(value);
    // }

    void return_void() { this->value = std::nullopt; }

    inline Generator<T> get_return_object() noexcept {
      return Generator{
          std::coroutine_handle<promise_type>::from_promise(*this)};
    }

    value_type get_value() { return std::move(value); }

    bool finished() {
      // return !value.has_value();
      return final;
    }

  private:
    value_type value{};
    bool final = false;
  };

  promise_type::value_type next() {
    if (_coroutine) {
      if (!_coroutine.promise().finished()) {
        _coroutine.resume();
      }
      return _coroutine.promise().get_value();
    } else {
      return {};
    }
  }

  struct end_iterator {};

  class iterator {
  public:
    using value_type = promise_type::value_type;
    using difference_type = std::ptrdiff_t;
    using iterator_category = std::input_iterator_tag;

    iterator() = default;
    iterator(Generator &generator) : generator{&generator} {}

    value_type operator*() const {
      if (generator) {
        return generator->_coroutine.promise().get_value();
      }
      return {};
    }

    value_type operator->() const {
      if (generator) {
        return generator->_coroutine.promise().get_value();
      }
      return {};
    }

    iterator &operator++() {
      if (generator && generator->_coroutine) {
        generator->_coroutine.resume();
      }
      return *this;
    }

    iterator &operator++(int) {
      if (generator && generator->_coroutine) {
        generator->_coroutine.resume();
      }
      return *this;
    }

    bool operator==(const end_iterator &) const {
      return !generator || generator->_coroutine.promise().finished();
    }

  private:
    Generator *generator{};
  };

  iterator begin() {
    iterator it{*this};
    return ++it;
  }

  end_iterator end() { return end_sentinel; }

  std::optional<value_type> py_next() { return next(); }

private:
  end_iterator end_sentinel{};
  std::coroutine_handle<promise_type> _coroutine;
};

} // namespace typon

#endif // TYPON_GENERATOR_HPP
