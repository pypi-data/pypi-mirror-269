//
// Created by Tom on 02/08/2023.
//

#ifndef TYPON_SLICE_HPP
#define TYPON_SLICE_HPP

#include <Python.h>
#include <optional>
#include <stdint.h>
#include <utility>

namespace typon {
using namespace referencemodel;

struct UnpackedSlice {
    ssize_t start, stop, step;
  };

template <typename _Base0 = object>
struct TySlice__oo : classtype<_Base0, TySlice__oo<>> {
  static constexpr std::string_view name = "TySlice";

  template <typename Start, typename Stop, typename Step>
  struct Obj : value<TySlice__oo<>, Obj<Start, Stop, Step>> {
    Start start;
    Stop stop;
    Step step;

    Obj(Start start, Stop stop, Step step)
        : start(start), stop(stop), step(step) {}

    std::pair<ssize_t, UnpackedSlice> adjust_indices(ssize_t seq_length) {
        UnpackedSlice res;

        if constexpr (std::is_same_v<Step, TyNone>) {
          res.step = 1;
        } else {
          res.step = this->step;
        }

        if constexpr (std::is_same_v<Start, TyNone>) {
          res.start = res.step < 0 ? PY_SSIZE_T_MAX : 0;
        } else {
          res.start = this->start;
        }

        if constexpr (std::is_same_v<Stop, TyNone>) {
          res.stop = res.step < 0 ? PY_SSIZE_T_MIN : PY_SSIZE_T_MAX;
        } else {
          res.stop = this->stop;
        }

        auto len =
            PySlice_AdjustIndices(seq_length, &res.start, &res.stop, res.step);

        return {len, res};
      }
  };

  template <typename Stop> auto operator()(Stop stop) const {
    return Obj<TyNone, Stop, TyNone>{None, stop, None};
  }

  template <typename Start, typename Stop>
  auto operator()(Start start, Stop stop) const {
    return Obj<Start, Stop, TyNone>{start, stop, None};
  }

  template <typename Start, typename Stop, typename Step>
  auto operator()(Start start, Stop stop, Step step) const {
    return Obj<Start, Stop, Step>{start, stop, step};
  }
};

static constexpr TySlice__oo<> TySlice{};

} // namespace typon
/*struct TySlice {
  TySlice() = default;
  TySlice(const TySlice &) = default;
  TySlice(TySlice &&) = default;
  TySlice &operator=(const TySlice &) = default;
  TySlice &operator=(TySlice &&) = default;

  TySlice(std::optional<ssize_t> start, std::optional<ssize_t> stop,
          std::optional<ssize_t> step)
      : start(start), stop(stop), step(step) {
    if (step == 0) {
      throw std::runtime_error("slice step cannot be zero");
    }
  }

  std::optional<ssize_t> start = 0;
  std::optional<ssize_t> stop = 0;
  std::optional<ssize_t> step = 1;




};*/

#endif // TYPON_SLICE_HPP
