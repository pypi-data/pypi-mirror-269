//
// Created by Tom on 13/03/2023.
//

#ifndef TYPON_RANGE_HPP
#define TYPON_RANGE_HPP

#include <ranges>

namespace view = std::views;

#include "int.hpp"
#include <python/basedef.hpp>

auto stride = [](int n) {
  return [s = -1, n](auto const &) mutable {
    s = (s + 1) % n;
    return !s;
  };
};

// todo: proper range support
struct range_s : TyBuiltin<range_s> {
  auto sync(int start, int stop, int step = 1) {
    // https://www.modernescpp.com/index.php/c-20-pythons-map-function/
    if (step == 0) {
      throw std::invalid_argument("Step cannot be 0");
    }
    auto Step = start < stop ? step : -step;
    auto Begin = std::min(start, stop);
    auto End = Step < 0 ? Begin : std::max(start, stop);
    return view::iota(Begin, End) | view::filter(stride(std::abs(Step))) |
           view::transform([start, stop](std::size_t i) {
             return typon::TyInt(start < stop ? i : stop - (i - start));
           });
  }

  auto sync(int stop) { return sync(0, stop); }

} range;

#endif // TYPON_RANGE_HPP
