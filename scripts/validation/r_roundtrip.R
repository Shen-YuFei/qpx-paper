# Read every QPX view into R data frames and write them back, for comparison in Python.
args <- commandArgs(trailingOnly = TRUE)
src <- args[1]
out <- args[2]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
for (f in list.files(src, pattern = "\\.parquet$", full.names = TRUE)) {
  df <- arrow::read_parquet(f)
  cat(basename(f), nrow(df), ncol(df), "\n")
  arrow::write_parquet(df, file.path(out, basename(f)))
}
cat("R", R.version.string, "arrow", as.character(packageVersion("arrow")), "\n")
