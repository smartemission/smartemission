
zooify <- function(df, col_time = "datetime") {
  idx <- df[, which(col_time %in% names(df))]
  df <- df[, -which(col_time %in% names(df))]
  df <- zoo(data.matrix(df), idx)
  return(df)
}

zoo_interpolate_left <- function(zoo1, zoo2, maxgap = 10) {
  z <- merge(zoo1, zoo2, all = TRUE)
  z <- na.approx(z, maxgap = maxgap)
  z <- z[index(zoo1), ]
  return(z)
}

remove_na_col <- function(df, max.part = 1.0, verbose = FALSE) {
  many_na <- colSums(is.na(df)) / nrow(df)
  if (verbose & sum(many_na >= max.part) > 0) {
    print("Deleting columns because of to many NA's")
    print(names(many_na[many_na >= max.part]))
  }
  df <- df[, many_na < max.part]
  return(df)
}

remove_constant_col <- function(df, min.var = 0.0, verbose = FALSE) {
  few_var <- sapply(df, var, na.rm = TRUE)
  few_var[is.na(few_var)] <- 0
  if (verbose & sum(few_var <= min.var)) {
    print("Deleting columns because of to few variance:")
    print(names(few_var[few_var <= min.var]))
  }
  df <- df[, few_var > min.var]
  return(df)
}

remove_related_col <- function(df, max.cor = 1.0, verbose = FALSE) {
  c <- cor(df, use = "pairwise.complete.obs") >= max.cor
  above_diag <- (row(c) - col(c)) > 0
  col_rm <- colSums(c & above_diag, na.rm = TRUE)
  if (verbose & sum(col_rm) > 0) {
    print("Deleting columns because to high correlation:")
    print(names(col_rm[col_rm > 0]))
  }
  df <- df[, -which(col_rm > 0)]
  return(df)
}