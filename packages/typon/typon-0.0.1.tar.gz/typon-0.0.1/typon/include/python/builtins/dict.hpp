//
// Created by Tom on 08/03/2023.
//

#ifndef TYPON_DICT_HPP
#define TYPON_DICT_HPP

#include <pybind11/stl.h>
#include <unordered_map>

/*
template <typename K, typename V>
class TyDict : public std::unordered_map<K, V> {
public:
  TyDict(std::unordered_map<K, V> &&m)
      : std::unordered_map<K, V>(std::move(m)) {}

  TyDict(std::initializer_list<std::pair<const K, V>> m)
      : std::unordered_map<K, V>(m) {}

  operator std::unordered_map<K, V>() const {
    return std::unordered_map<K, V>(this->begin(), this->end());
  }

  operator std::unordered_map<K, V> &() {
    return *reinterpret_cast<std::unordered_map<K, V> *>(this);
  }

  std::size_t py_len() const { return this->size(); }

  bool py_contains(const K &k) const { return this->find(k) != this->end(); }

  class iterator {
  public:
    using value_type = std::pair<K, V>;
    using difference_type = std::ptrdiff_t;
    using pointer = std::pair<K, V> *;
    using reference = std::pair<K, V> &;
    using iterator_category = std::forward_iterator_tag;

    iterator(typename std::unordered_map<K, V>::iterator it) : _it(it) {}

    iterator &operator++() {
      _it++;
      return *this;
    }

    iterator operator++(int) {
      iterator tmp = *this;
      _it++;
      return tmp;
    }

    bool operator==(const iterator &rhs) const { return _it == rhs._it; }

    bool operator!=(const iterator &rhs) const { return _it != rhs._it; }

    const std::pair<K, V> &operator*() const { return *_it; }

    const std::pair<K, V> *operator->() const { return &*_it; }

  private:
    typename std::unordered_map<K, V>::iterator _it;
  };

  iterator py_iter() const { return this->begin(); }

  void py_print(std::ostream &s) const {
    s << '{';
    if (this->size() > 0) {
      print_to(this->begin()->first, s);
      s << ": ";
      print_to(this->begin()->second, s);
      for (auto it = ++this->begin(); it != this->end(); it++) {
        s << ", ";
        print_to(it->first, s);
        s << ": ";
        print_to(it->second, s);
      }
    }
    s << '}';
  }
};

template <typename K, typename V>
TyDict(std::initializer_list<std::pair<K, V>>) -> TyDict<K, V>;*/

namespace typon {

/*template <typename K, typename V> class TyDict {
public:
  TyDict(std::shared_ptr<std::unordered_map<K, V>> &&m) : _m(std::move(m)) {}
  TyDict(std::unordered_map<K, V> &&m)
      : _m(std::move(
            std::make_shared<std::unordered_map<K, V>>(std::move(m)))) {}
  TyDict(std::initializer_list<std::pair<const K, V>> &&m)
      : _m(std::make_shared<std::unordered_map<K, V>>(std::move(m))) {}

  TyDict() : _m(std::make_shared<std::unordered_map<K, V>>()) {}
  template <typename... Args>
  TyDict(Args &&...args)
      : _m(std::make_shared<std::unordered_map<K, V>>(
            std::forward<Args>(args)...)) {}

  auto begin() const { return _m->begin(); }
  auto end() const { return _m->end(); }

  auto py_contains(const K &k) const { return _m->find(k) != _m->end(); }

  constexpr const V &operator[](const K &k) const { return (*_m)[k]; }
  constexpr V &operator[](const K &k) { return (*_m)[k]; }

  size_t py_len() const { return _m->size(); }

  void py_repr(std::ostream &s) const {
    s << '{';
    if (_m->size() > 0) {
      repr_to(_m->begin()->first, s);
      s << ": ";
      repr_to(_m->begin()->second, s);
      for (auto it = ++_m->begin(); it != _m->end(); it++) {
        s << ", ";
        repr_to(it->first, s);
        s << ": ";
        repr_to(it->second, s);
      }
    }
    s << '}';
  }

  void py_print(std::ostream &s) const { py_repr(s); }

private:
  std::shared_ptr<std::unordered_map<K, V>> _m;
};*/

} // namespace typon

/*namespace PYBIND11_NAMESPACE {
namespace detail {
template <typename K, typename V>
struct type_caster<typon::TyDict<K, V>>
    : map_caster<typon::TyDict<K, V>, K, V> {};
} // namespace detail
} // namespace PYBIND11_NAMESPACE*/

namespace typon {
using namespace referencemodel;
template <typename _Base0 = object>
struct TyDict__oo : classtype<_Base0, TyDict__oo<>> {

  struct : method {
    template <typename Self> auto operator()(Self self) const {
      std::stringstream s;
      s << '{';
      if (self->_m->size() > 0) {
        s << repr(self->_m->begin()->first)->value;
        s << ": ";
        s << repr(self->_m->begin()->second)->value;
        for (auto it = ++self->_m->begin(); it != self->_m->end(); it++) {
          s << ", ";
          s << repr(it->first)->value;
          s << ": ";
          s << repr(it->second)->value;
        }
      }
      s << '}';
      return typon::TyStr__oo<>::Obj(s.str());
    }
  } static constexpr oo__repr__oo{};

  static constexpr auto oo__str__oo = oo__repr__oo;

  template <typename K, typename V>
  struct Obj : instance<TyDict__oo<>, Obj<K, V>> {
    using map_type = std::unordered_map<K, V>;
    std::shared_ptr<map_type> _m;

    /*Obj(std::shared_ptr<std::unordered_map<K, V>> &&m) : _m(std::move(m)) {}
    Obj(std::unordered_map<K, V> &&m)
        : _m(std::move(
              std::make_shared<std::unordered_map<K, V>>(std::move(m)))) {}*/
    /*Obj(std::initializer_list<typename map_type::value_type> &&m)
        : _m(std::make_shared<map_type>(std::move(m))) {}*/
        Obj(std::initializer_list<std::pair<K, V>> && init)
          : _m(std::make_shared<std::unordered_map<K, V>>(init.begin(), init.end())) {}

    Obj() : _m(std::make_shared<map_type>()) {}
    template <typename... Args>
    Obj(Args &&...args)
        : _m(std::make_shared<map_type>(
              std::forward<Args>(args)...)) {}

    auto begin() const { return _m->begin(); }
    auto end() const { return _m->end(); }
  };

  template <typename T> auto operator()(std::initializer_list<T> &&v) const {
    return rc(Obj(std::move(v)));
  }

  template <typename... Args> auto operator()(Args &&...args) const {
    return rc(Obj(std::forward<Args>(args)...));
  }
};

static constexpr TyDict__oo<> TyDict{};

} // namespace typon

/*template <typename T> auto dict(std::initializer_list<T> &&v) {
  return typon::TyDict(std::move(v));
}*/

namespace PYBIND11_NAMESPACE {
namespace detail {
template <typename K, typename V>
struct type_caster<typon::TyDict__oo<>::Obj<K, V>>
    : map_caster<typon::TyDict__oo<>::Obj<K, V>, K, V> {};
} // namespace detail
} // namespace PYBIND11_NAMESPACE

#endif // TYPON_DICT_HPP
