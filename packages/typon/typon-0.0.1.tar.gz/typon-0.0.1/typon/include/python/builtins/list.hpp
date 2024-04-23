//
// Created by Tom on 08/03/2023.
//

#ifndef TYPON_LIST_HPP
#define TYPON_LIST_HPP

#include <algorithm>
#include <ostream>
#include <vector>
// #include <nanobind/stl/detail/nb_list.h>
#include <pybind11/stl.h>

namespace typon {
using namespace referencemodel;
template <typename _Base0 = object>
struct TyList__oo : classtype<_Base0, TyList__oo<>> {

  struct : method {
    auto operator()(auto self) const { return TyList__oo<>{}(self->_v); }
  } static constexpr copy{};

  struct : method {
    auto operator()(auto self, auto other) const {
      self->_v.reserve(self->_v.size() + other.size());
      self->_v.insert(self->_v.end(), other.begin(), other.end());
      return None;
    }
  } static constexpr extend{};

  // append
    struct : method {
        auto operator()(auto self, auto value) const { self->_v->push_back(value);
         return None;
         }
    } static constexpr append{};

  struct : method {
    auto operator()(auto self, auto other) const {
      auto result = TyList__oo<>{}(self->_v);
      dot(result, extend)(other);
      return result;
    }
  } static constexpr oo__add__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      auto result = TyList__oo<>{}(self->_v);
      result->_v->reserve(result->_v->size() * other);
      for (int i = 0; i < other - 1; i++) {
        dot(result, extend)(self);
      }
      return result;
    }
  } static constexpr oo__mul__oo{};

  struct : method {
    auto operator()(auto self) const {
      std::stringstream s;
      s << '[';
      if (self->_v->size() > 0) {
        s << repr(self->_v->operator[](0))->value;
        for (size_t i = 1; i < self->_v->size(); i++) {
          s << ", ";
          s << repr(self->_v->operator[](i))->value;
        }
      }
      s << ']';
      return typon::TyStr__oo<>::Obj(s.str());
    }
  } static constexpr oo__repr__oo{};

  static constexpr auto oo__str__oo = oo__repr__oo;

  struct : method {
    auto operator()(auto self) const { return typon::TyInt(self->_v->size()); }
  } static constexpr oo__len__oo{};

  // getitem
  struct : method {
    auto operator()(auto self, auto i) const {
      if (i < 0) {
        i += TyInt(self->_v->size());
      }
      if (i < 0 || i >= self->_v->size()) {
        throw std::out_of_range("list index out of range");
      }
      return self->_v->operator[](i);
    }
  } static constexpr oo__getitem__oo{};

  template <typename T> struct Obj : value<TyList__oo<>, Obj<T>> {
    using value_type = T;

    std::shared_ptr<std::vector<T>> _v;

    Obj(std::shared_ptr<std::vector<T>> &&v) : _v(std::move(v)) {}
    Obj(std::vector<T> &&v)
        : _v(std::move(std::make_shared<std::vector<T>>(std::move(v)))) {}
    Obj(std::initializer_list<T> &&v)
        : _v(std::make_shared<std::vector<T>>(std::move(v))) {}

    Obj() : _v(std::make_shared<std::vector<T>>()) {}

    void clear() { _v->clear(); }
    void push_back(const T &value) { _v->push_back(value); }
    size_t size() const { return _v->size(); }
    auto begin() const { return _v->begin(); }
    auto end() const { return _v->end(); }
  };

  template <typename T> auto operator()(std::initializer_list<T> &&v) const {
    return (Obj(std::move(v)));
  }

  template <typename... Args> auto operator()(Args &&...args) const {
    return (Obj(std::forward<Args>(args)...));
  }

  /*
  TyList(std::shared_ptr<std::vector<T>> &&v) : _v(std::move(v)) {}
  TyList(std::vector<T> &&v)
      : _v(std::move(std::make_shared<std::vector<T>>(std::move(v)))) {}

  TyList(std::initializer_list<T> &&v)
      : _v(std::make_shared<std::vector<T>>(std::move(v))) {}

  TyList() : _v(std::make_shared<std::vector<T>>()) {}

  auto begin() const { return _v->begin(); }

  auto end() const { return _v->end(); }

  METHOD(auto, append, (Self self, const T &x), {
    self._v->push_back(x);
  })

  METHOD(auto, py_contains, (Self self, const T &x), {
    return std::find(self.begin(), self.end(), x) != self.end();
  })

  auto size() const { return _v->size(); }

  void push_back(const T &value) { _v->push_back(value); }

  void clear() { _v->clear(); }*/

  /*operator std::vector<T>() const {
    return std::vector<T>(this->begin(), this->end());
  }

  operator std::vector<T> &() {
    return *reinterpret_cast<std::vector<T> *>(this);
  }*/

  /*constexpr const T &operator[](size_t i) const { return _v->operator[](i); }
  constexpr T &operator[](size_t i) { return _v->operator[](i); }

  size_t py_len() const { return _v->size(); }

  void py_repr(std::ostream &s) const {
    s << '[';
    if (_v->size() > 0) {
      repr_to(_v->operator[](0), s);
      for (size_t i = 1; i < _v->size(); i++) {
        s << ", ";
        repr_to(_v->operator[](i), s);
      }
    }
    s << ']';
  }

  void py_print(std::ostream &s) const { py_repr(s); }*/
};

static constexpr TyList__oo<> TyList{};

} // namespace typon

template <typename T> auto list(std::initializer_list<T> &&v) {
  return typon::TyList(std::move(v));
}

namespace PYBIND11_NAMESPACE {
namespace detail {
template <typename Type>
struct type_caster<typon::TyList__oo<>::Obj<Type>>
    : list_caster<typon::TyList__oo<>::Obj<Type>, Type> {};
} // namespace detail
} // namespace PYBIND11_NAMESPACE

/*NAMESPACE_BEGIN(NB_NAMESPACE)
NAMESPACE_BEGIN(detail)

template <typename Type> struct type_caster<TyList<Type>>
    : list_caster<TyList<Type>, Type> { };

NAMESPACE_END(detail)
NAMESPACE_END(NB_NAMESPACE)
*/
#endif // TYPON_LIST_HPP
