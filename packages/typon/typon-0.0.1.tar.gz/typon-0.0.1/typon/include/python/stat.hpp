//
// Created by Tom on 04/07/2023.
//

#ifndef TYPON_STAT_HPP
#define TYPON_STAT_HPP

#include "builtins.hpp"
#include <sys/stat.h>

#undef S_ISDIR
#undef S_ISREG
#undef S_ISLNK

namespace py_stat {
struct stat_t {
  FUNCTION(bool, S_ISDIR, (int mode), { return (mode & S_IFMT) == S_IFDIR; })
  FUNCTION(bool, S_ISREG, (int mode), { return (mode & S_IFMT) == S_IFREG; })
  FUNCTION(bool, S_ISLNK, (int mode), { return (mode & S_IFMT) == S_IFLNK; })
} all;

auto &get_all() { return all; }
} // namespace py_stat

#endif // TYPON_STAT_HPP
