//
// Created by Tom on 08/03/2023.
//

#ifndef TYPON_STR_HPP
#define TYPON_STR_HPP

#include <algorithm>
#include <sstream>
#include <string>

using namespace std::literals;

#include "slice.hpp"
// #include <format>
#include <fmt/format.h>
#include <pybind11/cast.h>

/*class TyStr : public std::string {
public:
  TyStr() : std::string() {}
  TyStr(const std::string &s) : std::string(s) {}
  TyStr(std::string &&s) : std::string(std::move(s)) {}
  constexpr TyStr(const char *s, size_t count) : std::string(s, count) {}
  constexpr TyStr(size_t count, char ch) : std::string(count, ch) {}
  template<typename... Args>
  TyStr(Args&&... args) : std::string(std::forward<Args>(args)...) {}

  template <class InputIterator>
  TyStr(InputIterator first, InputIterator last) : std::string(first, last) {}


  METHOD(TyBytes, encode, (Self self, const std::string &encoding = "utf-8"), {
        return TyBytes(self.begin(), self.end());
          })

  METHOD_GEN((typename... T), TyStr, format, (Self self, T &&...args), {
        return TyStr(fmt::format(fmt::runtime(self), std::forward<T>(args)...));
          })

  METHOD(bool, startswith, (Self self, const std::string &s), {
        return self.starts_with(s);
          })

  METHOD(int, find, (Self self, const std::string &s), {
        auto pos = self.std::string::find(s);
        return pos == std::string::npos ? -1 : pos;
          })

  METHOD(bool, isspace, (Self self), {
       return self.find_first_not_of(' ') == std::string::npos;
                                     })

  METHOD(auto, py_contains, (Self self, const std::string &x), {
    return self.std::string::find(x) != std::string::npos;
  })

  TyStr operator[](TySlice slice) const {
    auto [len, new_slice] = slice.adjust_indices(this->size());

    TyStr result;
    result.reserve(len);

    if (new_slice.start < new_slice.stop) {
      if (new_slice.step > 0) {
        for (auto i = new_slice.start; i < new_slice.stop;
             i += new_slice.step) {
          result.push_back(this->char_at(i));
        }
      }
    } else {
      if (new_slice.step < 0) {
        for (auto i = new_slice.start; i > new_slice.stop;
             i += new_slice.step) {
          result.push_back(this->char_at(i));
        }
      }
    }

    return result;
  }

  TyStr operator[](ssize_t index) const {
    if (index < 0) {
      index += this->size();
    }

    return TyStr(1, std::string::operator[](index));
  }

  char char_at(ssize_t index) const {
    if (index < 0) {
      index += this->size();
    }

    return this->begin()[index];
  }

  operator int() const {
    return std::stoi(*this);
  }
};

inline constexpr TyStr operator""_ps(const char *s, size_t len) noexcept {
  return TyStr(s, len);
}

template<typename Self>
TyStr TyBytes::decode_s::operator()(Self self, const std::string &encoding)
const { return TyStr(self.begin(), self.end());
}

template <typename T> TyStr str(const T &x) {
  std::stringstream s;
  print_to(x, s);
  return s.str();
}

template <typename T> TyStr repr(const T &x) {
  std::stringstream s;
  ::repr_to(x, s);
  return s.str();
}

template <> struct std::hash<TyStr> {
  std::size_t operator()(const TyStr &s) const noexcept {
    return std::hash<std::string>()(s);
  }
};

namespace PYBIND11_NAMESPACE {
namespace detail {
template<>
struct type_caster<TyStr>
    : string_caster<TyStr> {};
}}

template <> void repr_to(const TyStr &x, std::ostream &s) {
  s << '"' << x << '"';
}

template <> void print_to<TyStr>(const TyStr &x, std::ostream &s) { s << x; }

struct {
  TyStr operator()(const TyStr& s = ""_ps) {
    std::cout << s;
    TyStr input;
    std::getline(std::cin, input);
        return input;
  }
} input;*/

namespace typon {
using namespace referencemodel;
template <typename _Base0 = object>
struct TyStr__oo : classtype<_Base0, TyStr__oo<>> {
  static constexpr std::string_view name = "TyStr";

  struct : method {
    auto operator()(auto self, auto other) const {
      return Obj(dot(self, value) + dot(other, value));
    }
  } static constexpr oo__add__oo{};

  struct : method {
    auto operator()(auto self) const { return Obj(self->value); }
  } static constexpr oo__str__oo{};

  struct : method {
    auto operator()(auto self) const {
      return Obj(fmt::format("\"{}\"", self->value));
    }
  } static constexpr oo__repr__oo{};

  struct : method {
    auto operator()(auto self) const { return (self->value.size()); }
  } static constexpr oo__len__oo{};

  // getitem
  struct : method {
    template<typename T, typename U, typename V>
    auto operator()(auto self, TySlice__oo<>::Obj<T, U, V> slice) const {
      auto [len, new_slice] = slice.adjust_indices(self->value.size());
      Obj result;
      result.value.reserve(len);
      if (new_slice.start < new_slice.stop) {
        if (new_slice.step > 0) {
          for (auto i = new_slice.start; i < new_slice.stop;
               i += new_slice.step) {
            result.value.push_back(self->value[i]);
          }
        }
      } else {
        if (new_slice.step < 0) {
          for (auto i = new_slice.start; i > new_slice.stop;
               i += new_slice.step) {
            result.value.push_back(self->value[i]);
          }
        }
      }
      return result;
    }

    auto operator()(auto self, auto index) const {
      if (index < 0) {
        index += self->value.size();
      }
      return Obj(self->value[index]);
    }
  } static constexpr oo__getitem__oo{};

  struct : method {
      auto operator()(auto self, auto other) const {
      auto pos = self->value.find(other->value);
      return (pos == std::string::npos ? -1 : pos);
      }
  } static constexpr find{};

  struct : method {
    auto operator()(auto self, auto other) const {
      return self->value.starts_with(other->value);
    }
  } static constexpr startswith{};

  struct : method {
    auto operator()(auto self, auto encoding = Obj(std::string("utf-8"))) const {
      return Obj(self->value);
    }
  } static constexpr encode{};

  // format
  /*
    METHOD_GEN((typename... T), TyStr, format, (Self self, T &&...args), {
          return TyStr(fmt::format(fmt::runtime(self),
    std::forward<T>(args)...));
            })
            */

  struct : method {
    auto operator()(auto self, auto... args) const {
      return Obj(fmt::format(fmt::runtime(self->value), args...));
    }
  } static constexpr format{};

  struct Obj : value<TyStr__oo<>, Obj> {
    using value_type = std::string::value_type;
    std::string value;

    constexpr Obj() : value() {}
    constexpr Obj(std::string value) : value(value) {}
    constexpr Obj(const std::string_view &value) : value(value) {}
    constexpr Obj(const char* value) : value(value) {}
    constexpr Obj(const char* value, size_t count) : value(value, count) {}
    operator std::string() const { return value; }
    operator std::string_view() const { return value; }

    auto data() const { return value.data(); }
    auto size() const { return value.size(); }

    bool operator ==(const Obj &other) const { return value == other.value; }
  };

  auto operator()(std::string value) const { return Obj(value); }
};
static constexpr TyStr__oo<> TyStr{};

} // namespace typon

inline constexpr auto operator""_ps(const char *s, size_t len) noexcept {
  return typon::TyStr__oo<>::Obj(std::string(s, len));
}

template <> struct std::hash<decltype(""_ps)> {
  std::size_t operator()(const decltype(""_ps) &s) const noexcept {
    return std::hash<std::string>()(s);
  }
};

/*template <typename T> auto str(const T &x) { return dot(x, oo__str__oo)(); }

template <typename T>
concept NoStr = not requires(T x) { dot(x, oo__str__oo)(); };

template <NoStr T> auto str(const T &x) {
  std::stringstream s;
  s << x;
  return typon::TyStr__oo<>::Obj(s.str());
}
*/

template <typename T>
concept HasStr = requires(T x) { x->oo__str__oo; };

template <typename T>
concept HasRepr = requires(T x) { dot(x, oo__repr__oo)(); };

template <typename T>
concept HasRefModelRepresentation = requires {
   std::declval<T>()->repr;
};

template <typename T> auto str(const T &x) {
  if constexpr (HasStr<T>) {
    return dot(x, oo__str__oo)();
  } else if constexpr (HasRepr<T>) {
    return dot(x, oo__repr__oo)();
  } else if constexpr (HasRefModelRepresentation<T>) {
    return "<"_ps + typon::TyStr__oo<>::Obj(x->repr) + ">"_ps;
  } else {
    std::stringstream s;
    s << x;
    return typon::TyStr__oo<>::Obj(s.str());
  }
}

template <typename T> auto repr(const T &x) {
  if constexpr (HasRepr<T>) {
    return dot(x, oo__repr__oo)();
  } else if constexpr (HasRefModelRepresentation<T>) {
    return "<"_ps + typon::TyStr__oo<>::Obj(x->repr) + ">"_ps;
  } else {
    std::stringstream s;
    s << x;
    return typon::TyStr__oo<>::Obj(s.str());
  }
}

namespace PYBIND11_NAMESPACE {
namespace detail {
template<>
struct type_caster<decltype(""_ps)>
    : string_caster<decltype(""_ps)> {};
}}

#endif // TYPON_STR_HPP
