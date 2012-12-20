# autotab

experimental automatic tab completion for IPython by parsing numpy
formatted docstring. This goes along with IPython PR 2701

https://github.com/ipython/ipython/pull/2701

## examples

```
In [1]: import numpy as np

In [2]: import autotab

In [3]: autotab.install(np)

In [4]: np.zeros(not_evaluated).<TAB>
.T             .base          .copy          .dtype         .getfield      .min           .put           .searchsorted  .squeeze       .tolist
.all           .byteswap      .ctypes        .dump          .imag          .nbytes        .ravel         .setasflat     .std           .tostring
.any           .choose        .cumprod       .dumps         .item          .ndim          .real          .setfield      .strides       .trace
.argmax        .clip          .cumsum        .fill          .itemset       .newbyteorder  .repeat        .setflags      .sum           .transpose
.argmin        .compress      .data          .flags         .itemsize      .nonzero       .reshape       .shape         .swapaxes      .var
.argsort       .conj          .diagonal      .flat          .max           .prod          .resize        .size          .take          .view
.astype        .conjugate     .dot           .flatten       .mean          .ptp           .round         .sort          .tofile        
```
