#ifndef REFERENCEMODEL_H
#define REFERENCEMODEL_H

#include <array>
#include <atomic>
#include <cassert>
#include <concepts>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <string_view>
#include <type_traits>
#include <utility>

namespace referencemodel {

/* Object model forward declarations */

struct object;

template <typename T, typename O> struct instance;

template <typename T, typename O> struct value;

template <typename B, typename T> struct classtype;

template <typename M> struct moduletype;

struct function;

struct method;

struct classmethod;

struct staticmethod;

template <typename S, typename F> struct boundmethod;

/* Reference model forward declarations */

template <typename T> struct Pack;

template <typename T> struct Rc;

template <typename T> struct Arc;

template <typename T> struct Box;

template <typename T> struct Ref;

/* Meta-programming utilities */

namespace meta {

/* Meta-programming utilities: always_false */

template <typename T> struct always_false_s {
  constexpr static bool value{false};
};

template <typename T>
inline constexpr bool always_false = always_false_s<T>::value;

/* Meta-programming utilities: unwrap_one */

template <typename T> struct unwrap_one_s {
  using type = T;
};

template <typename T> struct unwrap_one_s<Pack<T>> {
  using type = T;
};

template <typename T> struct unwrap_one_s<Rc<T>> {
  using type = T;
};

template <typename T> struct unwrap_one_s<Arc<T>> {
  using type = T;
};

template <typename T> struct unwrap_one_s<Box<T>> {
  using type = T;
};

template <typename T> struct unwrap_one_s<Ref<T>> {
  using type = T;
};

template <typename T>
using unwrap_one = typename unwrap_one_s<std::remove_cvref_t<T>>::type;

/* Meta-programming utilities: unwrap_all */

template <typename T> struct unwrap_all_s {
  using type = unwrap_one<T>;
};

template <typename T> struct unwrap_all_s<Ref<Pack<T>>> {
  using type = T;
};

template <typename T> struct unwrap_all_s<Ref<Arc<T>>> {
  using type = T;
};

template <typename T> struct unwrap_all_s<Box<Pack<T>>> {
  using type = T;
};

template <typename T>
using unwrap_all = typename unwrap_all_s<std::remove_cvref_t<T>>::type;

/* Meta-programming utilities: unwrap_pack */

template <typename T> struct unwrap_pack_s {
  using type = unwrap_all<T>;
};

template <typename T> struct unwrap_pack_s<Pack<T>> {
  using type = Pack<T>;
};

template <typename T> struct unwrap_pack_s<Ref<Pack<T>>> {
  using type = Pack<T>;
};

template <typename T> struct unwrap_pack_s<Ref<Arc<T>>> {
  using type = Pack<T>;
};

template <typename T> struct unwrap_pack_s<Box<Pack<T>>> {
  using type = Pack<T>;
};

template <typename T>
using unwrap_pack = typename unwrap_pack_s<std::remove_cvref_t<T>>::type;

/* Meta-programming utilities for object model */

template <typename T>
concept object = std::derived_from<unwrap_all<T>, referencemodel::object>;

template <typename T>
concept instance = std::derived_from<
    unwrap_all<T>,
    referencemodel::instance<typename unwrap_all<T>::type, unwrap_all<T>>>;

template <typename T>
concept classtype =
    !instance<T> &&
    std::derived_from<unwrap_all<T>,
                      referencemodel::classtype<typename unwrap_all<T>::base,
                                                typename unwrap_all<T>::type>>;

template <typename F>
concept function = std::derived_from<F, referencemodel::function>;

template <typename F>
concept method = std::derived_from<F, referencemodel::method>;

template <typename F>
concept classmethod = std::derived_from<F, referencemodel::classmethod>;

template <typename F>
concept staticmethod = std::derived_from<F, referencemodel::staticmethod>;

template <typename T> struct boundmethod_s {
  static constexpr bool value = false;
};

template <typename S, typename F>
struct boundmethod_s<referencemodel::boundmethod<S, F>> {
  static constexpr bool value = true;
};

template <typename T>
concept boundmethod = boundmethod_s<std::remove_cvref_t<T>>::value;

template <typename T> struct value_s {
  static constexpr bool value = true;
};

template <instance T> struct value_s<T> {
  static constexpr bool value = std::derived_from<
      unwrap_all<T>,
      referencemodel::value<typename unwrap_all<T>::type, unwrap_all<T>>>;
};

template <typename S, typename F>
struct value_s<referencemodel::boundmethod<S, F>> {
  static constexpr bool value = value_s<S>::value;
};

template <typename T>
concept value = value_s<std::remove_cvref_t<T>>::value;

/* Meta-programming utilities: wrapped and unwrapped */

template <typename T>
concept unwrapped = std::is_same_v<T, unwrap_one<T>>;

template <typename T>
concept wrapped = !unwrapped<T>;

/* Meta-programming utilities: wrapped_by */

template <typename T, template <typename> typename M> struct wrapped_by_s {
  static constexpr bool value{false};
};

template <typename T, template <typename> typename M>
struct wrapped_by_s<M<T>, M> {
  static constexpr bool value{true};
};

template <typename T, template <typename> typename M>
concept wrapped_by = wrapped_by_s<std::remove_cvref<T>, M>::value;

/* Meta-programming utilities: pack */

template <typename T> struct pack_s {
  using type = Pack<unwrap_all<T>>;
};

template <value T> struct pack_s<T> {
  using type = T;
};

template <typename T> using pack = typename pack_s<T>::type;

/* Meta-programming utilities: rc */

template <typename T> struct rc_s {
  using type = Rc<unwrap_all<T>>;
};

template <value T> struct rc_s<T> {
  using type = T;
};

template <typename T> using rc = typename rc_s<T>::type;

/* Meta-programming utilities: arc */

template <typename T> struct arc_s {
  using type = Arc<unwrap_all<T>>;
};

template <value T> struct arc_s<T> {
  using type = T;
};

template <typename T> using arc = typename arc_s<T>::type;

/* Meta-programming utilities: box */

template <typename T> struct box_s {
  using type = Box<unwrap_pack<T>>;
};

template <value T> struct box_s<T> {
  using type = T;
};

template <typename T> using box = typename box_s<T>::type;

/* Meta-programming utilities: ref */

template <typename T> struct ref_s {
  using type = Ref<unwrap_all<T>>;
};

template <value T> struct ref_s<T> {
  using type = T;
};

template <typename T> using ref = typename ref_s<T>::type;

/* Meta-programming utilities: borrow */

template <typename T> struct borrow_s {
  using type = ref<T>;
};

template <typename T> struct borrow_s<Rc<T>> {
  using type = Ref<Pack<T>>;
};

template <typename T> struct borrow_s<Ref<Pack<T>>> {
  using type = Ref<Pack<T>>;
};

template <typename T> struct borrow_s<Arc<T>> {
  using type = Ref<Arc<T>>;
};

template <typename T> struct borrow_s<Ref<Arc<T>>> {
  using type = Ref<Arc<T>>;
};

template <typename T>
using borrow = typename borrow_s<std::remove_cvref_t<T>>::type;

/* Meta-programming utilities: forward */

template <typename T> struct forward_s {
  using type = borrow<T>;
};

template <typename T> struct forward_s<Box<T> &&> {
  using type = Box<T>;
};

template <typename T> using forward = typename forward_s<T>::type;

/* Meta-programming utilities: recover */

template <typename T> struct recover_s {
  using type = T;
};

template <value T> struct recover_s<T> {
  using type = T;
};

template <typename T> struct recover_s<Ref<Pack<T>>> {
  using type = Rc<T>;
};

template <typename T> struct recover_s<Ref<Arc<T>>> {
  using type = Arc<T>;
};

template <typename T>
using recover = typename recover_s<std::remove_cvref_t<T>>::type;

/* Meta-programming utilities: own */

template <typename T> struct own_s {
  using type = recover<T>;
};

template <unwrapped T> struct own_s<Ref<T>> {
  static_assert(always_false<T>, "Ref<T> cannot be owned");
};

template <typename T> using own = typename own_s<std::remove_cvref_t<T>>::type;

/* Meta-programming utilities: common_forward */

template <typename...> struct common_forward_s {};

template <typename... T>
using common_forward = typename common_forward_s<T...>::type;

template <typename T> struct common_forward_s<T> {
  using type = forward<T>;
};

template <typename T, typename U> struct common_forward_s<T, U> {
  using type = std::common_type_t<forward<T>, forward<U>>;
};

template <typename T> struct common_forward_s<T, T> {
  using type = forward<T>;
};

template <instance T, instance U>
  requires std::is_same_v<forward<T>, forward<U>>
struct common_forward_s<T, U> {
  using type = forward<T>;
};

template <instance T, instance U>
  requires std::is_same_v<unwrap_all<T>, unwrap_all<U>> &&
           (!std::is_same_v<forward<T>, forward<U>>)
struct common_forward_s<T, U> {
  static_assert(!std::is_same_v<T, Box<unwrap_all<T>> &&>);
  static_assert(!std::is_same_v<U, Box<unwrap_all<U>> &&>);
  using type = ref<T>;
};

template <typename T, typename U, typename... V>
struct common_forward_s<T, U, V...> {
  using type = common_forward<common_forward<T, U>, V...>;
};

} // namespace meta

/* Conversion functions */

template <typename T> auto pack(T &&t) {
  return meta::pack<T>(std::forward<T>(t));
}

template <typename T> auto rc(T &&t) { return meta::rc<T>(std::forward<T>(t)); }

template <typename T> auto arc(T &&t) {
  return meta::arc<T>(std::forward<T>(t));
}

template <typename T> auto box(T &&t) {
  return meta::box<T>(std::forward<T>(t));
}

template <typename T> auto ref(T &&t) {
  return meta::ref<T>(std::forward<T>(t));
}

template <typename T> auto borrow(T &&t) {
  return meta::borrow<T>(std::forward<T>(t));
}

template <typename T> auto forward(T &&t) {
  return meta::forward<T &&>(std::forward<T>(t));
}

template <typename T> auto recover(T &&t) {
  return meta::recover<T>(std::forward<T>(t));
}

template <typename T> auto own(T &&t) {
  return meta::own<T>(std::forward<T>(t));
}

/* Utilities: NonNull */

template <typename T> struct NonNull {
  NonNull() = default;

  NonNull(T *some) : ptr(some) { assert(ptr); };

  NonNull &operator=(const T *some) {
    ptr = some;
    assert(ptr);
    return *this;
  }

  NonNull(std::nullptr_t) : ptr(nullptr) {}

  NonNull &operator=(std::nullptr_t) {
    ptr = nullptr;
    return *this;
  }

  T *operator->() const { return ptr; }

  operator T *() const { return ptr; }

  operator bool() const { return ptr; }

private:
  T *ptr;
};

/* Reference model */

template <typename T> struct Pack {
  static_assert(std::is_same_v<T, meta::unwrap_all<T>>);
  static_assert(std::atomic_ref<std::uint32_t>::is_always_lock_free);

  Pack() = default;

  Pack(T &&t) : rc(1), value(std::move(t)) {}

  Pack(Pack &&) = default;

  const T *operator->() const { return std::addressof(value); }

  T *operator->() { return std::addressof(value); }

  auto read_count() const { return rc; }

  auto atomic_read_count() const {
    return std::atomic_ref(rc).load(std::memory_order_relaxed);
  }

  friend struct Rc<T>;
  friend struct Arc<T>;
  friend struct Box<Pack>;
  friend struct Ref<T>;
  friend struct Ref<Pack>;
  friend struct Ref<Arc<T>>;

private:
  std::uint32_t rc = 1;
  T value;
};

template <typename T> struct Rc {
  static_assert(std::is_same_v<T, meta::unwrap_all<T>>);

  Rc() : ptr(nullptr) {}

  Rc(std::nullptr_t) : ptr(nullptr) {}

  Rc(T &&t) : ptr(new Pack<T>(std::move(t))) {}

  Rc(Pack<T> &&pack) : ptr(new Pack<T>(std::move(pack))) {}

  Rc(Pack<T> &pack) : ptr(&pack) { ptr->rc++; }

  Rc(Rc &&rc) : ptr(std::exchange(rc.ptr, nullptr)) {}

  Rc(const Rc &rc) : ptr(rc.ptr) { ptr->rc++; }

  Rc(const Ref<Pack<T>> &ref) : ptr(ref.ptr) {
    assert(ptr->read_count());
    ptr->rc++;
  }

  Rc(Box<Pack<T>> &box) : ptr(std::exchange(box.ptr, nullptr)) {
    assert(!ptr->rc++);
  }

  Rc(Box<Pack<T>> &&box) : ptr(std::exchange(box.ptr, nullptr)) {
    assert(!ptr->rc++);
  }

  Rc &operator=(Rc rc) {
    std::swap(ptr, rc.ptr);
    return *this;
  }

  ~Rc() {
    if (ptr) { // null only if (swapped with a) moved from or uninitialised Rc
      if (!--(ptr->rc)) {
        delete ptr;
      }
    }
  }

  T *operator->() const { return std::addressof(ptr->value); }

  auto read_count() const { return ptr->read_count(); }

  friend struct Box<Pack<T>>;
  friend struct Ref<T>;
  friend struct Ref<Pack<T>>;

private:
  NonNull<Pack<T>> ptr;
};

template <typename T> struct Arc {
  static_assert(std::is_same_v<T, meta::unwrap_all<T>>);

  Arc() : ptr(nullptr) {}

  Arc(std::nullptr_t) : ptr(nullptr) {}

  Arc(std::in_place_t) : ptr(new Pack<T>()) {}

  Arc(T &&t) : ptr(new Pack<T>(std::move(t))) {}

  Arc(Arc &&arc) : ptr(std::exchange(arc.ptr, nullptr)) {}

  Arc(const Arc &arc) : ptr(arc.ptr) {
    std::atomic_ref(ptr->rc).fetch_add(1, std::memory_order_relaxed);
  }

  Arc(const Ref<Arc<T>> &ref) : ptr(ref.ptr) {
    assert(ptr->atomic_read_count());
    std::atomic_ref(ptr->rc).fetch_add(1, std::memory_order_relaxed);
  }

  Arc(Box<Pack<T>> &box) : ptr(std::exchange(box.ptr, nullptr)) {
    assert(!std::atomic_ref(ptr->rc).fetch_add(1, std::memory_order_relaxed));
  }

  Arc(Box<Pack<T>> &&box) : ptr(std::exchange(box.ptr, nullptr)) {
    assert(!std::atomic_ref(ptr->rc).fetch_add(1, std::memory_order_relaxed));
  }

  Arc &operator=(Arc arc) {
    std::swap(ptr, arc.ptr);
    return *this;
  }

  ~Arc() {
    if (ptr) { // null only if (swapped with a) moved from or uninitialised Arc
      if (std::atomic_ref(ptr->rc).fetch_sub(1, std::memory_order_release) ==
          1) {
        std::atomic_thread_fence(std::memory_order_acquire);
        delete ptr;
      }
    }
  }

  T *operator->() const { return std::addressof(ptr->value); }

  auto read_count() const { return ptr->atomic_read_count(); }

  friend struct Box<Pack<T>>;
  friend struct Ref<T>;
  friend struct Ref<Arc<T>>;

private:
  NonNull<Pack<T>> ptr;
};

template <typename T> struct Box {
  static_assert(std::is_same_v<T, meta::unwrap_all<T>>);

  Box() : ptr(nullptr) {}

  Box(std::nullptr_t) : ptr(nullptr) {}

  Box(T &&t) : ptr(new T(std::move(t))) {}

  Box(Box &box) : ptr(std::exchange(box.ptr, nullptr)) {}

  Box(Box &&box) : ptr(std::exchange(box.ptr, nullptr)) {}

  Box &operator=(Box box) {
    std::swap(ptr, box.ptr);
    return *this;
  }

  ~Box() {
    if (ptr) { // null only if (swapped with a) moved from or uninitialised Box
      delete ptr;
    }
  }

  T *operator->() const { return ptr; }

  friend struct Ref<T>;

private:
  NonNull<T> ptr;
};

template <typename T> struct Box<Pack<T>> {
  Box() : ptr(nullptr) {}

  Box(std::nullptr_t) : ptr(nullptr) {}

  Box(T &&t) : ptr(new Pack<T>(std::move(t))) { assert(!--(ptr->rc)); }

  Box(Pack<T> &&pack) : ptr(new Pack<T>(std::move(pack))) {
    assert(!--(ptr->rc));
  }

  Box(Rc<T> &&rc) : ptr(rc.ptr) { assert(!--(ptr->rc)); }

  Box(Arc<T> &&rc) : ptr(rc.ptr) {
    assert(std::atomic_ref(ptr->rc).fetch_sub(1, std::memory_order_relaxed) ==
           1);
  }

  Box(Box &box) : ptr(std::exchange(box.ptr, nullptr)) {}

  Box(Box &&box) : ptr(std::exchange(box.ptr, nullptr)) {}

  Box &operator=(Box box) {
    std::swap(ptr, box.ptr);
    return *this;
  }

  ~Box() {
    if (ptr) { // null only if (swapped with a) moved from or uninitialised Box
      delete ptr;
    }
  }

  T *operator->() const { return ptr; }

  friend struct Rc<T>;
  friend struct Arc<T>;
  friend struct Ref<T>;

private:
  NonNull<Pack<T>> ptr;
};

template <typename T> struct Ref {
  static_assert(std::is_same_v<T, meta::unwrap_all<T>>);

  Ref() = default;

  Ref(T &t) : ptr(std::addressof(t)) {}

  Ref(const Ref &) = default;
  Ref(Ref &&) = default;

  Ref &operator=(Ref ref) {
    ptr = ref.ptr;
    return *this;
  }

  Ref(Pack<T> &pack) : ptr(std::addressof(pack.value)) {}

  Ref(const Rc<T> &rc) : ptr(std::addressof(rc.ptr->value)) {}

  Ref(const Arc<T> &arc) : ptr(std::addressof(arc.ptr->value)) {}

  Ref(const Ref<Pack<T>> &ref) : ptr(std::addressof(ref.ptr->value)) {}

  Ref(const Ref<Arc<T>> &ref) : ptr(std::addressof(ref.ptr->value)) {}

  Ref(const Box<T> &box) : ptr(box.ptr) {}

  Ref(const Box<Pack<T>> &box) : ptr(box.ptr) {}

  T *operator->() const { return ptr; }

private:
  NonNull<T> ptr;
};

template <typename T> struct Ref<Pack<T>> {
  Ref() = default;

  Ref(Pack<T> &pack) : ptr(std::addressof(pack)) {}

  Ref(const Ref &) = default;
  Ref(Ref &&) = default;

  Ref &operator=(Ref ref) {
    ptr = ref.ptr;
    return *this;
  }

  Ref(const Rc<T> &rc) : ptr(rc.ptr) {}

  T *operator->() const { return std::addressof(ptr->value); }

  friend struct Rc<T>;
  friend struct Ref<T>;

private:
  NonNull<Pack<T>> ptr;
};

template <typename T> struct Ref<Arc<T>> {
  Ref() = default;

  Ref(const Ref &) = default;
  Ref(Ref &&) = default;

  Ref &operator=(Ref ref) {
    ptr = ref.ptr;
    return *this;
  }

  Ref(const Arc<T> &arc) : ptr(arc.ptr) {}

  T *operator->() const { return std::addressof(ptr->value); }

  friend struct Arc<T>;
  friend struct Ref<T>;

private:
  NonNull<Pack<T>> ptr;
};

template <typename T> Ref(Rc<T> &) -> Ref<T>;

template <typename T> Ref(Rc<T> &&) -> Ref<T>;

template <typename T> Ref(Arc<T> &) -> Ref<T>;

template <typename T> Ref(Arc<T> &&) -> Ref<T>;

template <typename T> Ref(Box<T> &) -> Ref<meta::unwrap_all<T>>;

template <typename T> Ref(Box<T> &&) -> Ref<meta::unwrap_all<T>>;

template <meta::wrapped T> Ref(Ref<T> &) -> Ref<meta::unwrap_all<T>>;

template <meta::wrapped T> Ref(Ref<T> &&) -> Ref<meta::unwrap_all<T>>;

/* Equality */

template <typename T, typename U>
  requires meta::wrapped<T> || meta::wrapped<U>
bool operator==(const T &t, const U &u) {
  return t.operator->() == u.operator->();
}

namespace meta {

/* Compile-time string concatenation */

// taken from https://stackoverflow.com/a/62823211

template <std::string_view const &...Strs> struct join_s {
  // Join all strings into a single std::array of chars
  static constexpr auto impl() noexcept {
    constexpr std::size_t len = (Strs.size() + ... + 0);
    std::array<char, len + 1> arr{};
    auto append = [i = 0, &arr](auto const &s) mutable {
      for (auto c : s)
        arr[i++] = c;
    };
    (append(Strs), ...);
    arr[len] = 0;
    return arr;
  }
  // Give the joined string static storage
  static constexpr auto arr = impl();
  // View as a std::string_view
  static constexpr std::string_view value{arr.data(), arr.size() - 1};
};

template <std::string_view const &...Strs>
static constexpr auto join = join_s<Strs...>::value;

} // namespace meta

/* Object model */

struct object {
  template <typename T, typename O> friend struct instance;

  template <typename B, typename T> friend struct classtype;

  template <typename M> friend struct moduletype;

private:
  static constexpr std::string_view object_of_ = "object of ";
  static constexpr std::string_view class_ = "class ";
  static constexpr std::string_view module_ = "module ";
};

template <typename T, typename O> struct instance : T {
  using type = T;

  static constexpr std::string_view repr =
      meta::join<object::object_of_, T::repr>;

  const O *operator->() const { return static_cast<const O *>(this); }
  O *operator->() { return static_cast<O *>(this); }
};

template <typename T, typename O> struct value : instance<T, O> {};

template <typename B, typename T> struct classtype : B {
  using base = B;
  using type = T;

  static constexpr std::string_view repr = meta::join<object::class_, T::name>;

  const T *operator->() const { return static_cast<const T *>(this); }
  T *operator->() { return static_cast<T *>(this); }
};

namespace meta {

/* Class rebasing */

template <typename T> struct rebase_s {
  static_assert(always_false<T>, "Cannot rebase this type");
};

template <template <typename> typename Class, typename Base>
struct rebase_s<Class<Base>> {
  template <typename Rebase> using type = Class<Rebase>;
};

template <typename T, typename Rebase>
using rebase = typename rebase_s<std::remove_cvref_t<T>>::template type<Rebase>;

} // namespace meta

template <typename M> struct moduletype : object {
  using type = M;

  static constexpr std::string_view repr = meta::join<object::module_, M::name>;

  const M *operator->() const { return static_cast<const M *>(this); }
  M *operator->() { return static_cast<M *>(this); }
};

struct function {};

struct method : function {};

struct classmethod : function {};

struct staticmethod : function {};

template <typename S, typename F> struct boundmethod : object {
  using Self = S;
  using Func = F;

  boundmethod() = default;

  boundmethod(boundmethod &) = default;
  boundmethod(boundmethod &&) = default;
  boundmethod &operator=(boundmethod &) = default;
  boundmethod &operator=(boundmethod &&) = default;

  template <typename T>
  boundmethod(const boundmethod<T, F> &m) : self(m.self), func(m.func) {}

  template <typename T>
  boundmethod(boundmethod<T, F> &&m) : self(std::move(m.self)), func(m.func) {}

  template <typename T> boundmethod &operator=(boundmethod<T, F> &m) {
    func = m.func;
    self = m.self;
    return *this;
  }

  template <typename T> boundmethod &operator=(boundmethod<T, F> &&m) {
    func = std::move(m.func);
    self = std::move(m.self);
    return *this;
  }

  template <typename... Args> auto operator()(Args &&...args) & {
    return func(forward(self), std::forward<Args>(args)...);
  }

  template <typename... Args> auto operator()(Args &&...args) && {
    return func(forward(std::move(self)), std::forward<Args>(args)...);
  }

  template <typename T, typename G> friend struct boundmethod;

  template <meta::instance T, meta::method G> friend auto bind(T &&, const G &);

  template <meta::classtype T, meta::classmethod G>
  friend auto bind(T &&, const G &);

  template <meta::instance T, meta::classmethod G>
  friend auto bind(T &&, const G &);

  const F &_func_() const { return func; }

  const S &_self_() const { return self; }

private:
  template <typename T>
  boundmethod(T &&self, F func) : self(std::forward<T>(self)), func(func) {}

  [[no_unique_address]] S self;
  [[no_unique_address]] F func;
};

namespace meta {

/* Specialisations for boundmethod */

template <boundmethod T> struct pack_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<pack<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct rc_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<rc<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct arc_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<arc<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct box_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<box<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct ref_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<ref<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct borrow_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<borrow<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct forward_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<forward<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct forward_s<T &&> {
  using U = std::remove_cvref_t<T>;
  using type = referencemodel::boundmethod<forward<typename U::Self &&>,
                                           typename U::Func>;
};

template <boundmethod T> struct recover_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<recover<typename U::Self>, typename U::Func>;
};

template <boundmethod T> struct own_s<T> {
  using U = std::remove_cvref_t<T>;
  using type =
      referencemodel::boundmethod<own<typename U::Self>, typename U::Func>;
};

} // namespace meta

/* Attribute access with on-the-fly method binding */

template <meta::instance S, meta::method F> auto bind(S &&self, const F &func) {
  return boundmethod<meta::forward<S &&>, F>(std::forward<S>(self), func);
}

template <meta::classtype S, meta::classmethod F>
auto bind(S &&self, const F &func) {
  return boundmethod<std::remove_cvref_t<S>, F>{self, func};
}

template <meta::instance S, meta::classmethod F>
auto bind(S &&, const F &func) {
  using type = typename meta::unwrap_all<S>::type;
  static_assert(sizeof(type) == 1);
  return boundmethod<type, F>{type{}, func};
}

template <typename S, typename A, typename... T>
decltype(auto) bind(S &&, A &attr, T...) {
  return attr;
}

#define dot(OBJ, NAME)                                                         \
  [](auto &&obj) -> decltype(auto) {                                           \
    return referencemodel::bind(std::forward<decltype(obj)>(obj), obj->NAME);  \
  }(OBJ)

/* Operators */

namespace meta {

// note: using dot here would cause hard failure instead of invalid constraint

/* + */

#define LR_OP(OP, DUNDER)                                                      \
  namespace meta {                                                             \
  template <typename Left, typename Right>                                     \
  concept Left##DUNDER##able = requires(Left left, Right right) {              \
    left->oo__##DUNDER##__oo(left, right);                                     \
  };                                                                           \
                                                                               \
  template <typename Left, typename Right>                                     \
  concept Right##DUNDER##able = requires(Left left, Right right) {             \
    right->oo__r##DUNDER##__oo(right, left);                                   \
  };                                                                           \
  template <typename Left, typename Right>                                     \
  concept Aug##DUNDER##able = requires(Left left, Right right) {               \
    left->oo__i##DUNDER##__oo(left, right);                                    \
  };                                                                           \
                                                                               \
  template <typename Left, typename Right>                                     \
  concept DUNDER##able =                                                       \
      Left##DUNDER##able<Left, Right> || Right##DUNDER##able<Left, Right>;     \
  template <typename Left, typename Right>                                     \
  concept NormalOrAug##DUNDER##able =                                          \
      DUNDER##able<Left, Right> || Aug##DUNDER##able<Left, Right>;             \
  }                                                                            \
  template <meta::object Left, meta::object Right>                             \
    requires meta::DUNDER                                                      \
  ##able<Left, Right> auto operator OP(Left &&left, Right &&right) {           \
    if constexpr (meta::Left##DUNDER##able<Left, Right>) {                     \
      return dot(std::forward<Left>(left),                                     \
                 oo__##DUNDER##__oo)(std::forward<Right>(right));              \
    } else {                                                                   \
      if constexpr (meta::Right##DUNDER##able<Left, Right>) {                  \
        return dot(std::forward<Right>(right),                                 \
                   oo__r##DUNDER##__oo)(std::forward<Left>(left));             \
      }                                                                        \
    }                                                                          \
  }                                                                            \
  template <meta::object Left, meta::object Right>                             \
    requires meta::NormalOrAug                                                 \
  ##DUNDER##able<Left, Right> auto operator OP##=(Left &&left,                 \
                                                  Right &&right) {             \
    if constexpr (meta::Aug##DUNDER##able<Left, Right>) {                      \
      return dot(std::forward<Left>(left),                                     \
                 oo__i##DUNDER##__oo)(std::forward<Right>(right));             \
    } else {                                                                   \
      return (left = (left OP right));                                         \
    }                                                                          \
  }

#define SIMPLE_OP(OP, DUNDER)                                                  \
  namespace meta {                                                             \
  template <typename Left, typename Right>                                     \
  concept DUNDER##able = requires(Left left, Right right) {                    \
    left->oo__##DUNDER##__oo(left, right);                                     \
  };                                                                           \
  }                                                                            \
  template <meta::object Left, meta::object Right>                             \
    requires meta::DUNDER                                                      \
  ##able<Left, Right> auto operator OP(Left &&left, Right &&right) {           \
    return dot(std::forward<Left>(left),                                       \
               oo__##DUNDER##__oo)(std::forward<Right>(right));                \
  }

/*template <typename Left, typename Right>
concept LeftAddable = requires (Left left, Right right) {
  left->oo__add__oo(left, right);
};

template <typename Left, typename Right>
concept RightAddable = requires (Left left, Right right) {
  // note: using dot here would cause hard failure instead of invalid constraint
  right->oo__radd__oo(right, left);
};

template <typename Left, typename Right>
concept Addable = LeftAddable<Left, Right> || RightAddable<Left, Right>;*/

} // namespace meta

/* + */

/*template <meta::object Left, meta::object Right>
  requires meta::Addable<Left, Right>
auto operator + (Left && left, Right && right) {
  if constexpr (meta::LeftAddable<Left, Right>) {
    return dot(std::forward<Left>(left), oo__add__oo)(
      std::forward<Right>(right));
  }
  else {
    if constexpr (meta::RightAddable<Left, Right>) {
      return dot(std::forward<Right>(right), oo__radd__oo)(
        std::forward<Left>(left));
    }
  }
}
*/

LR_OP(+, add)
LR_OP(-, sub)
LR_OP(*, mul)
LR_OP(/, truediv)
LR_OP(%, mod)
LR_OP(<<, lshift)
LR_OP(>>, rshift)
LR_OP(&, and)
LR_OP(^, xor)
LR_OP(|, or)

// TODO: iadd...

SIMPLE_OP(<, lt)
SIMPLE_OP(<=, le)
SIMPLE_OP(==, eq)
SIMPLE_OP(!=, ne)
SIMPLE_OP(>, gt)
SIMPLE_OP(>=, ge)

namespace meta {
template <typename Left, typename Right>
concept DUNDERgetitemable =
    requires(Left left, Right right) { left->oo__getitem__oo(left, right); };
template <typename Left, typename Right>
concept DUNDERsetitemable =
    requires(Left left, Right right) { left->oo__setitem__oo(left, right); };

} // namespace meta
/* template <meta::object Left, meta::object Right>
   requires meta::DUNDERgetitemable<Left, Right> auto operator [](Left &&left,
 Right &&right) {   return dot(std::forward<Left>(left),
              oo__getitem__oo)(std::forward<Right>(right));
 }*/
// todo: setitem?

} // namespace referencemodel

#endif // REFERENCEMODEL_H
