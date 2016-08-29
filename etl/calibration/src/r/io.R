
read_rivm <- function(folder, file, nrow = -1) {
  colType <- c("Begintijd" = "character", "Eindtijd" = "character")
  df <- fread(file.path(folder, file), colClasses = colType, nrows = nrow)
  df <- prefix_columns(df, c(3:6, 19:22), "Druk")
  df <- prefix_columns(df, c(7:10, 23:26), "CO")
  df <- prefix_columns(df, c(11:14, 27:30), "NO2")
  df <- prefix_columns(df, c(15:18, 35:38), "T")
  df <- prefix_columns(df, 31:34, "O3")
  df <- rename(df, c("Begintijd" = "datetime"), warn_duplicated = FALSE)
  df$datetime <- dmy_hm(df$datetime)
  df$Eindtijd <- dmy_hm(df$Eindtijd)
  df <- delete_suffix_columns(df)
  return(df)
}

read_jose <- function(folder, file, nrow = -1) {
  df <- fread(file.path(folder, file),
                 colClasses = c("datetime" = "character"),
                 nrows = nrow)
  df$datetime <- ymd_hms(df$datetime)
  df <- df[order(df$datetime), ]
  return(df)
}

prefix_columns <- function(df, cols, prefix) {
  names(df)[cols] <- paste(prefix, names(df)[cols], sep = "_")
  return(df)
}

delete_suffix_columns <- function(df, sep = ".") {
  f <- function(x) {strsplit(x, ".", fixed = TRUE)[[1]][1]}
  names(df) <- unlist(lapply(names(df), FUN = f))
  return(df)
}
