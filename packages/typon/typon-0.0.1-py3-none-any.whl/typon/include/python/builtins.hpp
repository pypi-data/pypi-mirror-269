//
// Created by Tom on 07/03/2023.
//

#ifndef TYPON_BUILTINS_HPP
#define TYPON_BUILTINS_HPP

#include <fmt/format.h>
#include <iostream>
#include <optional>
#include <ostream>
#include <string>

#include <python/basedef.hpp>

#include <typon/typon.hpp>

#ifdef __cpp_lib_unreachable
#include <utility>
[[noreturn]] inline void TYPON_UNREACHABLE() { std::unreachable(); }
#else
#include <cstdlib>
[[noreturn]] inline void TYPON_UNREACHABLE() { std::abort(); }
#endif

#define _Args(...) __VA_ARGS__
#define COMMA() ,
#define METHOD(ret, name, args, ...)                                           \
  static constexpr struct name##_s                                             \
      : referencemodel::method{template <typename Self> ret operator()         \
                                   args const __VA_ARGS__} name {};

#define METHOD_GEN(gen, ret, name, args, ...)                                  \
  static constexpr struct name##_s                                             \
      : referencemodel::method{                                                \
            template <typename Self, _Args gen> ret operator()                 \
                args const __VA_ARGS__} name {};

#define FUNCTION(ret, name, args, ...)                                         \
  struct : referencemodel::staticmethod {                                      \
    ret operator() args const __VA_ARGS__                                      \
  } static constexpr name{};

using namespace std::literals;

template <typename T>
concept PySmartPtr = requires { typename T::element_type; };

template <typename T>
concept PyUserType = requires { typename T::py_type; };

template <typename T> struct RealType {
  using type = T;
};

template <PyUserType T> struct RealType<T> {
  using type = typename T::py_type;
};

template <PySmartPtr T> struct RealType<T> {
  using type = typename T::element_type;
};

namespace typon {

// class TyNone {};

//using TyNone = std::nullopt_t;

struct TyNone {
    operator bool() const { return false; }
    operator std::nullopt_t() const { return std::nullopt; }
    template <typename T>
    operator std::optional<T>() const { return std::nullopt; }
};

auto None = TyNone{};

} // namespace typon

static constexpr auto None = typon::None;

// typon_len

template <typename T>
concept PyIterator = requires(T t) {
  { t.py_next() } -> std::same_as<std::optional<T>>;
};

template <typename T>
concept PyIterable = requires(T t) {
  { t.py_iter() } -> PyIterator;
};

template <PyIterable T, PyIterator U> U iter(const T &t) { return t.py_iter(); }

/*template <typename T>
concept CppSize = requires(const T &t) {
                    { t.size() } -> std::same_as<size_t>;
                  };

template <typename T>
concept PyLen = requires(const T &t) {
                  { t.py_len() } -> std::same_as<size_t>;
                };

template <CppSize T>
  requires(!PyLen<T>)
auto len(const T &t) {
  return t.size();
}

template <PyLen T> size_t len(const T &t) { return t.py_len(); }*/

template <typename T> auto len(T &&t) {
  return dot(std::forward<T>(t), oo__len__oo)();
}

template <typename T>
concept PyNext = requires(T t) {
  { t.py_next() } -> std::same_as<std::optional<typename T::value_type>>;
};

struct {
  template <PyNext T>
  std::optional<typename T::value_type>
  operator()(T &t, std::optional<typename T::value_type> def = std::nullopt) {
    auto opt = t.py_next();
    return opt ? opt : def;
  }
} next;

template <typename T>
std::ostream &operator<<(std::ostream &os, std::optional<T> const &opt) {
  return opt ? os << opt.value() : os << "None";
}

#define system_error(err, message)                                             \
  do {                                                                         \
    puts(message);                                                             \
    throw fmt::system_error(err, message);                                     \
  } while (0)

// #include "builtins/complex.hpp"
#include "builtins/bool.hpp"
#include "builtins/bytes.hpp"
#include "builtins/dict.hpp"
#include "builtins/int.hpp"
#include "builtins/list.hpp"
#include "builtins/mutex.hpp"
#include "builtins/print.hpp"
#include "builtins/range.hpp"
#include "builtins/set.hpp"
#include "builtins/slice.hpp"
#include "builtins/str.hpp"

auto is_cpp() { return typon::TyBool(true); }

namespace typon {
using namespace referencemodel;
template <typename _Base0 = object>
struct TyFile__oo : classtype<_Base0, TyFile__oo<>> {
  struct : method {
    Task<TyStr__oo<>::Obj> operator()(auto self, size_t size = -1) {
      if (size == -1) {
        size = self->len;
      }
      std::string buf(size, '\0');
      int nbytes = co_await typon::io::read(self->fd, buf.data(), size);
      if (nbytes < 0) {
        system_error(-nbytes, "read()");
      }
      buf.resize(nbytes);
      co_return std::move(TyStr__oo<>::Obj(buf));
    }
  } static constexpr read{};

  struct : method {
    Task<TyInt__oo<>::Obj> operator()(auto self, auto buf) {
      int nbytes = co_await typon::io::write(self->fd, buf->value);
      if (nbytes < 0) {
        system_error(-nbytes, "write()");
      }
      co_return TyInt(nbytes);
    }
  } static constexpr write{};

  struct : method {
    Task<void> operator()(auto self) { co_await typon::io::close(self->fd); }
  } static constexpr close{};

  struct : method {
    Task<void> operator()(auto self) { co_await typon::io::fsync(self->fd); }
  } static constexpr flush{};

  struct Obj : instance<TyFile__oo<>, Obj> {
    Obj(int fd = -1, size_t len = 0) : fd(fd), len(len) {}

    Obj(const Obj &other) : fd(other.fd), len(other.len) {}

    int fd;
    size_t len;
  };

  struct : method {
    auto operator()(auto self) { return self; }
  } static constexpr __enter__{};

  struct : method {
    Task<bool> operator()(auto self) {
      co_await dot(self, close)();
      co_return true;
    }
  } static constexpr __exit__{};
};

static constexpr TyFile__oo<> TyFile{};

} // namespace typon

typon::Task<typon::TyFile__oo<>::Obj> open(auto path, std::string_view mode) {
  const char *path_c = path->value.c_str();
  size_t len = 0;
  struct statx statxbuf;
  if (int err = co_await typon::io::statx(AT_FDCWD, path_c, 0, STATX_SIZE,
                                          &statxbuf)) {
    // new file
  } else {
    len = statxbuf.stx_size;
  }
  int flags = 0;
  bool created = false, writable = false, readable = false;

  if (mode.find('x') != std::string_view::npos) {
    created = true;
    writable = true;
    flags = O_EXCL | O_CREAT;
  } else if (mode.find('r') != std::string_view::npos) {
    readable = true;
    flags = 0;
  } else if (mode.find('w') != std::string_view::npos) {
    writable = true;
    flags = O_CREAT | O_TRUNC;
  } else if (mode.find('a') != std::string_view::npos) {
    writable = true;
    flags = O_APPEND | O_CREAT;
  }

  if (mode.find('+') != std::string_view::npos) {
    readable = true;
    writable = true;
  }

  if (readable && writable) {
    flags |= O_RDWR;
  } else if (readable) {
    flags |= O_RDONLY;
  } else {
    flags |= O_WRONLY;
  }

  flags |= O_CLOEXEC;

  int fd = co_await typon::io::openat(AT_FDCWD, path_c, flags, 0666);
  if (fd < 0) {
    std::cerr << path_c << "," << flags << std::endl;
    system_error(-fd, "openat()");
  }
  co_return typon::TyFile__oo<>::Obj(fd, len);
}

#include <typon/generator.hpp>

#include <pybind11/embed.h>
#include <pybind11/stl.h>
namespace py = pybind11;

#include <utility>

template <typename Ref> struct lvalue_or_rvalue {

  Ref &&ref;

  template <typename Arg>
  constexpr lvalue_or_rvalue(Arg &&arg) noexcept : ref(std::move(arg)) {}

  constexpr operator Ref &() const & noexcept { return ref; }
  constexpr operator Ref &&() const && noexcept { return std::move(ref); }
  constexpr Ref &operator*() const noexcept { return ref; }
  constexpr Ref *operator->() const noexcept { return &ref; }
};

namespace typon {
template <class... Types> using PyTuple = std::tuple<Types...>;

}

template <typename T> auto &iter_fix_ref(T &obj) { return obj; }

template <PySmartPtr T> auto &iter_fix_ref(T &obj) { return *obj; }

namespace std {
template <class T> auto begin(std::shared_ptr<T> &obj) {
  return dot(obj, begin)();
}

template <class T> auto end(std::shared_ptr<T> &obj) { return dot(obj, end)(); }
} // namespace std

template <typename T> struct AlwaysTrue { // (1)
  constexpr bool operator()(const T &) const { return true; }
};
/*template <typename Seq>
struct ValueTypeEx {
  using type = decltype(*std::begin(std::declval<Seq>()));
};*/

// has ::iterator type

template <typename T> struct ValueType {
  using type = decltype(*std::declval<T>().begin());
};

template <typename T>
concept HasIterator = requires(T t) { typename T::iterator; };

template <HasIterator T> struct ValueType<T> {
  using type = typename T::iterator::value_type;
};

// (2)
/*template <typename Map, typename Seq, typename Filt = AlwaysTrue<typename
ValueTypeEx<Seq>::type>> typon::Task< mapFilter(Map map, Seq seq, Filt filt =
Filt()) {

  //typedef typename Seq::value_type value_type;
  using value_type = typename ValueTypeEx<Seq>::type;
  using return_type = decltype(map(std::declval<value_type>()));

  std::vector<return_type> result{};
    for (auto i : seq) {
        if (co_await filt(i)) {
            result.push_back(co_await map(i));
        }
    }
  return typon::TyList(std::move(result));
}*/

#define MAP_FILTER(item, seq, map, filter)                                     \
  ({                                                                           \
    using value_type = ValueType<decltype(seq)>::type;                         \
    value_type item;                                                           \
    std::vector<decltype(map)> result{};                                       \
    for (auto item : seq) {                                                    \
      if (filter) {                                                            \
        result.push_back(map);                                                 \
      }                                                                        \
    }                                                                          \
    typon::TyList(std::move(result));                                          \
  })

namespace PYBIND11_NAMESPACE {
namespace detail {
template <typename T> struct type_caster<typon::Task<T>> {
  using type = typon::Task<T>;
  using res_conv = make_caster<T>;

public:
  PYBIND11_TYPE_CASTER(type,
                       const_name("Task[") + res_conv::name + const_name("]"));

  template <typename U>
  static handle cast(U &&src, return_value_policy policy, handle parent) {
    return res_conv::cast(std::forward<T>(std::move(src).call()), policy,
                          parent);
  }
};
} // namespace detail
} // namespace PYBIND11_NAMESPACE

#ifdef TYPON_EXTENSION
class InterpGuard {
  PyThreadState *main;
  PyThreadState *sub;

public:
  InterpGuard() {
    /*main = PyThreadState_Get();
    sub = Py_NewInterpreter();*/
  }

  ~InterpGuard() {
    /*Py_EndInterpreter(sub);
    PyThreadState_Swap(main);*/
  }
};
#else
using InterpGuard = py::scoped_interpreter;
#endif

template <typename T>
concept HasSync = requires(T t) { typename T::has_sync; };

template <typename T> struct HasBoundSync_t {
  static constexpr bool value = false;
};

template <typename S, typename F> struct HasBoundSync_t<referencemodel::boundmethod<S, F>> {
  static constexpr bool value = HasSync<F>;

  auto operator()(auto... args) {
    return F{}.typon$$sync(S{}, std::forward<decltype(args)>(args)...);
  }
};

template <typename T>
concept HasBoundSync = HasBoundSync_t<T>::value;

/*auto call_sync(auto f, auto... args) {
  if constexpr (HasSync<decltype(f)>) {
    return f.sync(std::forward<decltype(args)>(args)...);
  } else {
    return f(std::forward<decltype(args)>(args)...);
  }
}*/

auto call_sync(auto f) {
  if constexpr (HasSync<decltype(f)>) {
    return [f](auto... args) {
      return f.typon$$sync(std::forward<decltype(args)>(args)...);
    };
  } else if constexpr (HasBoundSync<decltype(f)>) {
    return HasBoundSync_t<decltype(f)>{};
  } else {
    return f;
  }
}

namespace typon {
template <auto IDX, typename T> auto constant_get(T &&val) {
  if constexpr (requires { std::get<IDX>(std::forward<T>(val)); }) {
    return std::get<IDX>(std::forward<T>(val));
  } else {
    return dot(std::forward<T>(val), oo__getitem__oo)(IDX);
  }
}

struct {
  using has_sync = std::true_type;

  template <typename T>
  auto typon$$sync(T value) const
      -> decltype(referencemodel::Rc(future(std::declval<Task<T>>()))) {
    // return referencemodel::Rc(future(task));
    throw;
  }

  template <typename Task>
  auto operator()(Task task) const
      -> typon::Task<decltype(referencemodel::Rc(future(std::move(task))))> {
    co_return referencemodel::Rc(co_await future(std::move(task)));
  }
} static constexpr future_stdlib{};

}; // namespace typon

#endif // TYPON_BUILTINS_HPP
