//
// Created by Tom on 04/07/2023.
//

#ifndef TYPON_IO_HPP
#define TYPON_IO_HPP

namespace py_io {
struct io_t {
  static constexpr int DEFAULT_BUFFER_SIZE = 8192;
} all;

auto &get_all() { return all; }
} // namespace py_io

#endif // TYPON_IO_HPP
