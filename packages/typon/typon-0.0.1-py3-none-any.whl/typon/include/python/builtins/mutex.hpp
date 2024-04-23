
#ifndef TYPON_MUTEX_HPP
#define TYPON_MUTEX_HPP

#include <ranges>

namespace view = std::views;

#include "str.hpp"
#include <python/basedef.hpp>

namespace typon {
using namespace referencemodel;

template <typename _Base0 = object>
struct TyCell__oo : classtype<_Base0, TyCell__oo<>> {
  static constexpr std::string_view name = "Cell";

  template <typename T> struct Obj : instance<TyCell__oo<>, Obj<T>> {
    T val;

    Obj() = default;
    Obj(Obj const &) = delete;
  };

  template <typename T> auto operator()(T val) const { return Obj<T>{val}; }

  struct : method {
      auto operator()(auto self) const {
        std::stringstream s;
        s << "Cell(" << repr(self->val)->value << ')';
        return typon::TyStr__oo<>::Obj(s.str());
      }
    } static constexpr oo__str__oo{};
};

template <typename _Base0 = object>
struct TyMutex__oo : classtype<_Base0, TyMutex__oo<>> {
  static constexpr std::string_view name = "Mutex";

  template <typename T> struct Obj : instance<TyMutex__oo<>, Obj<T>> {
    typon::Mutex mutex;
    TyCell__oo<>::Obj<T> cell;
  };

  struct : method {
    using has_sync = std::true_type;
    auto typon$$sync(auto, auto) -> TyNone const { return None; }

    auto operator()(auto _self, auto callback) -> typon::Task<TyNone> const {
      auto self = arc(_self);
      auto lock = dot(self, mutex).lock();
      co_await lock;
      co_await callback(ref(dot(self, cell)));
      co_return None;
    }
  } static constexpr when{};

  template <typename T> auto operator()(T val) const {
    auto obj = referencemodel::meta::arc<Obj<T>>(std::in_place);
    dot(obj, cell).val = val;
    return obj;
  }
};

template <typename T> using ArcMutex = Arc<TyMutex__oo<>::template Obj<T>>;

} // namespace typon

static constexpr typon::TyMutex__oo<> Mutex;

#endif // TYPON_MUTEX_HPP
