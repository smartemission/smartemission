
read_rivm <- function(folder, file, nrow = -1) {
  colType <- c("Begintijd" = "character", "Eindtijd" = "character")
  df <- read.csv(file.path(folder, file), colClasses = colType, nrow = nrow)
  df <- rename(df, c("Begintijd" = "datetime"))
  df <- prefix_columns(df, c(3:6, 19:22), "Druk")
  df <- prefix_columns(df, 7:10, "CO")
  df <- prefix_columns(df, c(11:14, 23:26), "NO2")
  df <- prefix_columns(df, c(15:18, 31:34), "T")
  df <- prefix_columns(df, 27:30, "O3")
  d_format <- "%d-%m-%Y %H:%M"
  df$datetime <- strptime(df$datetime, format = d_format)
  df$Eindtijd <- strptime(df$Eindtijd, format = d_format)
  df <- delete_suffix_columns(df)
  return(df)
}

read_jose <- function(folder, file, nrow = -1) {
  df <- read.csv(file.path(folder, file), header = FALSE, 
                 col.names = c("datetime", "Column", "Value"),
                 colClasses = c("datetime"="character"), 
                 nrow = nrow)
  df$datetime <- as.character(df$datetime)
  df <- reshape(df, timevar = "Column", idvar = "datetime", direction = "wide")
  d_format <- "%m/%d/%Y %H:%M:%S"
  df$datetime <- strptime(df$datetime, format = d_format)
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