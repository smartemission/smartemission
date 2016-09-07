library(ggplot2)
library(dplyr)
library(tidyr)

source("C.R")

load(file.path(folder, "rivm_jose_12_14.rda"))

## Uptime ----
df12 <- jose_12 %>%
  select(datetime, s.coresistance, s.no2resistance, s.o3resistance) %>%
  gather(gas, value, s.coresistance, s.no2resistance, s.o3resistance) %>%
  filter(!is.na(value)) %>%
  mutate(id = "Ruyterstraat")
df14 <- jose_14 %>%
  select(datetime, s.coresistance, s.no2resistance, s.o3resistance) %>%
  gather(gas, value, s.coresistance, s.no2resistance, s.o3resistance) %>%
  filter(!is.na(value)) %>%
  mutate(id = "Graafseweg")
df <- rbind(df12, df14)
df <- unite(df, gas, id, gas, sep = " ")

# df <- df[sample(1:nrow(df), 150000),]
ggplot(df, aes(x = datetime, y = gas)) +
  geom_jitter(size = .1) +
  theme_bw() +
  xlab("") +
  ylab("")
