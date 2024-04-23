//
// Created by Tom on 08/03/2023.
//

#ifndef TYPON_COMPLEX_HPP
#define TYPON_COMPLEX_HPP

#include <complex>
#include <ostream>

#include "print.hpp"

using TyComplex = std::complex<double>;

TyComplex operator+(int a, const TyComplex &b) { return TyComplex(a) + b; }

TyComplex operator-(int a, const TyComplex &b) { return TyComplex(a) - b; }

template <> void print_to<TyComplex>(const TyComplex &x, std::ostream &s) {
  if (x.real() == 0) {
    s << x.imag() << "j";
  } else {
    s << '(' << x.real() << "+" << x.imag() << "j)";
  }
}

#endif // TYPON_COMPLEX_HPP
