jose_12_feb <- read.csv("12.txt", header = FALSE)
jose_14_feb <- read.csv("14.txt", header = FALSE)
jose_12_14_after_feb <- read.csv("/home/pieter/Data/GemeenteNijmegen/SmartEmission/JoseneNijmegen2016-2.csv")

library(data.table)
df12 <- data.table(jose_12_feb)
df14 <- data.table(jose_14_feb)
dfboth <- data.table(jose_12_14_after_feb)

audio_values12 <- grepfilter("Audio", levels(df12$V2))
idx12 <- df12$V2 %in% audio_values12
df12_ <- df12[!idx12,]
audio_values14 <- grepfilter("Audio", levels(df14$V2))
idx14 <- df14$V2 %in% audio_values14
df14_ <- df14[!idx14,]
df12 <- df12_
df14 <- df14_

idx12 <- unite(df12, id, V1, V2)
idx12 <- duplicated(idx12$id)
df12_ <- df12[!idx12,]
idx14 <- unite(df14, id, V1, V2)
idx14 <- duplicated(idx14$id)
df14_ <- df14[!idx14,]

df12_ <- spread(df12_, V2, V3)
df14_ <- spread(df14_, V2, V3)
