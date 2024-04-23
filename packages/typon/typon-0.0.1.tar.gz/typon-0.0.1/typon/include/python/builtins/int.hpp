//
// Created by Tom on 08/03/2023.
//

#ifndef TYPON_INT_HPP
#define TYPON_INT_HPP

#include <algorithm>
#include <sstream>
#include <string>

using namespace std::literals;

#include "str.hpp"
// #include <format>
#include <fmt/format.h>
#include <pybind11/cast.h>

namespace typon {
using namespace referencemodel;

template <typename _Base0 = object>
struct TyInt__oo : classtype<_Base0, TyInt__oo<>> {
  static constexpr std::string_view name = "TyInt";

  struct : method {
    auto operator()(auto self, auto other) const {
      return Obj(dot(self, value) + dot(other, value));
    }
  } static constexpr oo__add__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return Obj(dot(self, value) - dot(other, value));
    }
  } static constexpr oo__sub__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return Obj(dot(self, value) * dot(other, value));
    }
  } static constexpr oo__mul__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return Obj(dot(self, value) & dot(other, value));
    }
  } static constexpr oo__and__oo{};

  struct : method {
    auto operator()(auto self) const { return Obj(-dot(self, value)); }
  } static constexpr oo__neg__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return TyBool(dot(self, value) < dot(other, value));
    }
  } static constexpr oo__lt__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return (dot(self, value) > dot(other, value));
    }
  } static constexpr oo__gt__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return TyInt(dot(self, value) % dot(other, value));
    }
  } static constexpr oo__mod__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return TyBool(dot(self, value) >= dot(other, value));
    }
  } static constexpr oo__ge__oo{};

  struct : method {
    auto operator()(auto self) const {
      return TyStr__oo<>::Obj(std::to_string(self->value));
    }
  } static constexpr oo__str__oo{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return TyBool(dot(self, value) == dot(other, value));
    }
  } static constexpr oo__eq__oo{};

  static constexpr auto oo__repr__oo = oo__str__oo;

  struct Obj : value<TyInt__oo<>, Obj> {
    int value;

    Obj(int value = 0) : value(value) {}
    Obj(std::string_view value) : value(std::stoi(std::string(value))) {}
    Obj(const Obj &other) : value(other.value) {}
    operator int() const { return value; }
  };

  auto operator()(auto value) const { return Obj(value); }
};
static constexpr TyInt__oo<> TyInt{};

} // namespace typon

inline auto operator""_pi(unsigned long long int v) noexcept {
  return typon::TyInt(v);
}

template <> struct std::hash<decltype(0_pi)> {
  std::size_t operator()(const decltype(0_pi) &s) const noexcept {
    return std::hash<int>()(s);
  }
};

namespace PYBIND11_NAMESPACE {
namespace detail {
template <> struct type_caster<decltype(0_pi)> {



public:
        /**
         * This macro establishes the name 'inty' in
         * function signatures and declares a local variable
         * 'value' of type inty
         */
        PYBIND11_TYPE_CASTER(decltype(0_pi), const_name("TyInt"));

        /**
         * Conversion part 1 (Python->C++): convert a PyObject into a inty
         * instance or return false upon failure. The second argument
         * indicates whether implicit conversions should be applied.
         */
        bool load(handle src, bool) {
            /* Extract PyObject from handle */
            PyObject *source = src.ptr();
            /* Try converting into a Python integer value */
            PyObject *tmp = PyNumber_Long(source);
            if (!tmp)
                return false;
            /* Now try to convert into a C++ int */
            dot(value, value) = PyLong_AsLong(tmp);
            Py_DECREF(tmp);
            /* Ensure return code was OK (to avoid out-of-range errors etc) */
            return !(dot(value, value) == -1 && !PyErr_Occurred());
        }

        /**
         * Conversion part 2 (C++ -> Python): convert an inty instance into
         * a Python object. The second and third arguments are used to
         * indicate the return value policy and parent object (for
         * ``return_value_policy::reference_internal``) and are generally
         * ignored by implicit casters.
         */
        static handle cast(auto src, return_value_policy /* policy */, handle /* parent */) {
            return PyLong_FromLong(dot(src, value));
        }





};
} // namespace detail
} // namespace PYBIND11_NAMESPACE

#endif // TYPON_INT_HPP
