## Libraries, sources and fixed variables -------------
library(tidyr)
library(ggplot2)
library(plyr)
library(compositions)
library(zoo)
library(grid)
library(gridExtra)
library(data.table)
library(lubridate)

source("io.R")
source("preproc.R")
source("interpolate.R")
source("C.R")
# source("features.R")

folder <- "~/Data/GemeenteNijmegen/SmartEmission"
nrow <- -1

## Load RIVM data -------------------------------------
rivm <- read_rivm(folder, "741_742_minuten_feb_jul2016.csv", nrow)
rivm_14 <- rivm[, c(1, 2, 3:18), with = FALSE]
rivm_12 <- rivm[, c(1, 2, 19:34), with = FALSE]
rivm_14 <- rivm_remove_bad_status(rivm_14)
rivm_12 <- rivm_remove_bad_status(rivm_12)

## Read jose data -------------------------------------
jose_12 <- read_jose(folder, "jose12.csv", nrow)
jose_14 <- read_jose(folder, "jose14.csv", nrow)
jose_12 <- preproc_jose(jose_12)
jose_14 <- preproc_jose(jose_14)
# jose_12 <- preproc_jose_types(jose_12)
# jose_14 <- preproc_jose_types(jose_14)
jose_12 <- preproc_jose_bad_values(jose_12, min.date = "2016-02-10")
jose_14 <- preproc_jose_bad_values(jose_14)
jose_12 <- jose_12[datetime > ymd_hms("20160401010101"), s.coresistance := NA]

## Save and reload data ------------------------------------------
save(rivm_14,
     rivm_12,
     jose_14,
     jose_12,
     file = file.path(folder, "rivm_jose_12_14.rda"))
load(file.path(folder, "rivm_jose_12_14.rda"))

## Interpolate data -----------------------------------------------------------
jose_12 <- jose_12[!duplicated(datetime),]
jose_14 <- jose_14[!duplicated(datetime),]
jose_12 <- remove_na_col(jose_12)
jose_14 <- remove_na_col(jose_14)
rivm_12 <- remove_na_col(rivm_12)
rivm_14 <- remove_na_col(rivm_14)

jose_12$secs <- as.numeric(format(jose_12$datetime, "%Y%m%d%H%M%S"))
jose_14$secs <- as.numeric(format(jose_14$datetime, "%Y%m%d%H%M%S"))

z_jose_12 <- zooify(jose_12)
z_jose_14 <- zooify(jose_14)
z_rivm_12 <- zooify(rivm_12)
z_rivm_14 <- zooify(rivm_14)

z_both_12 <- zoo_interpolate_left(z_jose_12, z_rivm_12)
z_both_14 <- zoo_interpolate_left(z_jose_14, z_rivm_14)

## Save and reload data --------------------------------------------------------
f_name <- "rivm_jose_interp_12_14.rda"
save(z_both_12, z_both_14, file = file.path(folder, f_name))
load(file.path(folder, f_name))

## Features --------------------------------------------------------------------
# df_12 <- preproc_jose_types(data.table(z_both_12))
# df_14 <- preproc_jose_types(data.table(z_both_14))
df_12 <- data.table(z_both_12)
df_14 <- data.table(z_both_14)
air <- rbind.fill(df_12, df_14)

air_jose <- air[, 1:26]
air_rivm <- air[, 27:47]

save(air, air_jose, air_rivm, file = file.path(folder, "rivm_jose_df_feat.rda"))

## CSV -------------------------------------------------------------------------
load(file.path(folder, "rivm_jose_df_feat.rda"))

csv.air <- air_jose[, grep("baro|co2|humidity|no2res|o3res|temp|secs|serial", colnames(air_jose))]

csv.air <- data.table(na.approx(csv.air, maxgap = 100, na.rm = TRUE))
na.idx <- rowSums(is.na(csv.air)) == 0
csv.air <- cbind(csv.air[na.idx,], air_rivm[na.idx, c("O3_Waarden", "NO2_Waarden", "CO_Waarden")])
csv.air$CO_Waarden[csv.air$CO_Waarden < 0] <- NA
csv.air$CO_Waarden[csv.air$CO_Waarden > 2000] <- NA
csv.air$NO2_Waarden[csv.air$NO2_Waarden < 0] <- NA
csv.air$NO2_Waarden[csv.air$NO2_Waarden > 250] <- NA
csv.air$O3_Waarden[csv.air$O3_Waarden < 0] <- NA
csv.air$O3_Waarden[csv.air$O3_Waarden > 200] <- NA


write.csv(csv.air, file = file.path(folder, "train.csv"), row.names = FALSE)
