# These files contain all the results from both benchmarks.

The naming convention is as follows:

```
case_<#>_[<nfp>, <nfp_rot>, <LO>, <convex>].svg
```

where:

* `<#>` is the case number
* `<nfp>` is `True` when the No Fit Polygon was used and False when the smallest enclosing circle method was used
* `<nfp_rot>` is the number of shape rotations for which the NFP was constructed
* `<LO>` is `True` when the local optmisation algorithm was used
* `<Convex>` is `True`, when the complicated shape's convex convex hull was used instead

The files `case_<#>_results.txt` contains the numerical results of all the test cases.