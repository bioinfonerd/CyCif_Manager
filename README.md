# rnmicro

The content is built automatically by Travis-CI and served on the `gh-pages` branch. You can build a local copy using the `bookdown` package in R:

``` r
if( !require(bookdown) ) install.packages("bookdown")
bookdown::render_book("index.md")
```
