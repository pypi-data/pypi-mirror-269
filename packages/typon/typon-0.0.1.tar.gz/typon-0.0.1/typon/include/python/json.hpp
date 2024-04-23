//
// Created by Tom on 04/07/2023.
//

#ifndef TYPON_JSON_HPP
#define TYPON_JSON_HPP

#include "builtins.hpp"

namespace py_json {
struct json_t {
  FUNCTION(template <typename T> typon::Task<void>, dump,
           (const T &x, typon::PyFile &fp), {
             std::stringstream ss;
             repr_to(x, ss);
             co_await dotp(fp, write)(ss.str());
           })
} all;

auto &get_all() { return all; }
} // namespace py_json

#endif // TYPON_JSON_HPP
