//
// Created by Tom on 09/03/2023.
//

#ifndef TYPON_PRINT_HPP
#define TYPON_PRINT_HPP

#include <functional>
#include <iostream>
#include <ostream>
#include <typon/typon.hpp>

/*template <typename T>
concept Streamable = requires(const T &x, std::ostream &s) {
  { s << x } -> std::same_as<std::ostream &>;
};

template <Streamable T> void print_to(const T &x, std::ostream &s) { s << x; }
template <Streamable T> void repr_to(const T &x, std::ostream &s) { s << x; }

template <typename T>
concept PyPrint = requires(const T &x, std::ostream &s) {
  { x.py_print(s) } -> std::same_as<void>;
};

template <PyPrint T> void print_to(const T &x, std::ostream &s) {
  x.py_print(s);
}

template <typename T>
concept TyRepr = requires(const T &x, std::ostream &s) {
  { x.py_repr(s) } -> std::same_as<void>;
};

template <TyRepr T> void repr_to(const T &x, std::ostream &s) { x.py_repr(s); }

template <typename T>
concept Printable = requires(const T &x, std::ostream &s) {
  { print_to(x, s) } -> std::same_as<void>;
};

template <typename T>
concept Reprable = requires(const T &x, std::ostream &s) {
  { repr_to(x, s) } -> std::same_as<void>;
};*/

template <typename T>
concept FunctionPointer =
    std::is_function_v<T> or std::is_member_function_pointer_v<T> or
    std::is_function_v<std::remove_pointer_t<T>>;

/*template <Streamable T>
  requires(FunctionPointer<T>)
void repr_to(const T &x, std::ostream &s) {
  s << "<function at 0x" << std::hex << (size_t)x << std::dec << ">";
}

template <typename T>
void repr_to(const std::function<T> &x, std::ostream &s) {
  s << "<function at 0x" << std::hex << (size_t)x.template target<T*>() <<
std::dec
    << ">";
}

template <Streamable T>
  requires(Reprable<T>)
void print_to(const T &x, std::ostream &s) {
  repr_to(x, s);
}

template <Printable T>
void print_to(const std::shared_ptr<T> &x, std::ostream &s) {
  print_to(*x, s);
}

template <Reprable T>
void repr_to(const std::shared_ptr<T> &x, std::ostream &s) {
  repr_to(*x, s);
}*/

/*
template <Printable T, Printable... Args>
typon::Task<void> print(T const &head, Args const &...args) {
  print_to(head, std::cout);
  (((std::cout << ' '), print_to(args, std::cout)), ...);
  std::cout << '\n'; co_return;
}*/

struct {
  typon::TyNone operator()() {
    std::cout << '\n';
    return typon::None;
  }

  template <typename T, typename... Args>
  typon::TyNone operator()(T const &head, Args const &...args) {
    std::cout << str(head)->value;
    (((std::cout << ' '), (std::cout << str(args)->value)), ...);
    std::cout << '\n';
    return typon::None;
  }
} print;
// typon::Task<void> print() { std::cout << '\n'; co_return; }

#endif // TYPON_PRINT_HPP
