//
// Created by Tom on 08/03/2023.
//

#ifndef TYPON_SET_HPP
#define TYPON_SET_HPP

#include <unordered_set>

namespace typon {

template <typename T> class TySet : public std::unordered_set<T> {
public:
  TySet(std::unordered_set<T> &&s) : std::unordered_set<T>(std::move(s)) {}

  TySet(std::initializer_list<T> &&s) : std::unordered_set<T>(std::move(s)) {}

  operator std::unordered_set<T>() const {
    return std::unordered_set<T>(this->begin(), this->end());
  }

  std::size_t py_len() const { return this->size(); }

  bool py_contains(const T &t) const { return this->find(t) != this->end(); }

  class iterator {
  public:
    using value_type = T;
    using difference_type = std::ptrdiff_t;
    using pointer = T *;
    using reference = T &;
    using iterator_category = std::forward_iterator_tag;

    iterator(typename std::unordered_set<T>::iterator it) : _it(it) {}

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

    const T &operator*() const { return *_it; }

    const T *operator->() const { return &*_it; }

  private:
    typename std::unordered_set<T>::iterator _it;
  };

  iterator py_iter() const { return this->begin(); }

  void py_print(std::ostream &s) const {
    s << '{';
    if (this->size() > 0) {
      print_to(*this->begin(), s);
      for (auto it = ++this->begin(); it != this->end(); it++) {
        s << ", ";
        print_to(*it, s);
      }
    }
    s << '}';
  }
};

} // namespace typon

template <typename T> typon::TySet<T> set(std::initializer_list<T> &&s) {
  return typon::TySet<T>(std::move(s));
}

#endif // TYPON_SET_HPP
