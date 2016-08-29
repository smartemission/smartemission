library(data.table)
library(handypandy)
library(tidyr)
library(plyr)

setwd("~/Data/GemeenteNijmegen/SmartEmission")

df12 <- fread("12.txt", header = FALSE)
df14 <- fread("14.txt", header = FALSE)
dfboth <- fread("JoseneNijmegen2016-3.csv")

audio_values12 <- grepfilter("Audio", levels(df12$V2))
audio_values14 <- grepfilter("Audio", levels(df14$V2))
idx12 <- df12$V2 %in% audio_values12
idx14 <- df14$V2 %in% audio_values14
df12 <- df12[!idx12,]
df14 <- df14[!idx14,]

idx12 <- unite(df12, id, V1, V2)
idx14 <- unite(df14, id, V1, V2)
idx12 <- duplicated(idx12$id)
idx14 <- duplicated(idx14$id)
df12 <- df12[!idx12,]
df14 <- df14[!idx14,]

df12 <- spread(df12, V2, V3)
df14 <- spread(df14, V2, V3)

dfboth <- rename(dfboth, c("Id" = "P.UnitSerialnumber",
                           "Time" = "datetime"))
df12 <- rename(df12, c("V1" = "datetime"))
df14 <- rename(df14, c("V1" = "datetime"))

var_names <- Reduce(intersect, lapply(list(df12, df14, dfboth), names))
dfboth <- dfboth[, var_names, with = FALSE]
df12 <- df12[, var_names, with = FALSE]
df14 <- df14[, var_names, with = FALSE]

df <- rbind(dfboth, df12, df14)

jose12 <- df[P.UnitSerialnumber == 12,]
jose14 <- df[P.UnitSerialnumber == 14,]

write.csv(jose12, "jose12.csv")
write.csv(jose14, "jose14.csv")
