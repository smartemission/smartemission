rivm_remove_bad_status <- function(df) {
  if ("Druk_Status" %in% names(df))
    df$Druk_Waarden[df$Druk_Status != 0 | df$Druk_Status.1 != 0] <- NA
  if ("NO2_Status" %in% names(df))
    df$NO2_Waarden[df$NO2_Status != 0 | df$NO2_Status.1 != 0 | df$NO2_Waarden < 0] <- NA
  if ("O3_Status" %in% names(df))
    df$O3_Waarden[df$O3_Status != 0 | df$O3_Status.1 != 0 | df$O3_Waarden < 0] <- NA
  if ("T_Status" %in% names(df))
    df$T_Waarden[df$T_Status != 0 | df$T_Status.1 != 0] <- NA
  if ("CO_Status" %in% names(df))
    df$CO_Waarden[df$CO_Status != 0 | df$CO_Status.1 != 0 | df$CO_Waarden< 0] <- NA
  return(df)
}

preproc_jose <- function(df) {
  # S.Longitude remove 0
  # s.Latitude remove 0
  # S.CO2 remove 0
  # For all, compute floats from int, read documentation sensors
  df <- cbind(df, jose_preproc_power_state(df$Value.P.Powerstate))
  df$Value.P.Powerstate <- NULL
  
  df <- cbind(df, jose_preproc_error_state(df$Value.P.ErrorStatus))
  df$Value.P.ErrorStatus <- NULL
  
  df <-
    cbind(df,
          jose_preproc_split_mode(df$Value.P.COHeaterMode, "p.co.heater"))
  df$Value.P.COHeaterMode <- NULL
  df <-
    cbind(df, jose_preproc_split_mode(df$Value.P.11, "p.no2.heater"))
  df$Value.P.11 <- NULL
  
  df$Value.S.RtcDate <- NULL
  df$Value.S.RtcTime <- NULL
  
  df$Value.S.TemperatureUnit <-
    (df$Value.S.TemperatureUnit / 1000.0) - 273.15
  df$Value.S.TemperatureAmbient <-
    (df$Value.S.TemperatureAmbient / 1000.0) - 273.15
  
  df$Value.S.Humidity <- df$Value.S.Humidity / 1000.0 # %RH
  
  df$Value.S.Barometer <- df$Value.S.Barometer / 100.0
  
  df$Value.S.AcceleroX <- (df$Value.S.AcceleroX - 512.0) / 256.0
  df$Value.S.AcceleroY <- (df$Value.S.AcceleroY - 512.0) / 256.0
  df$Value.S.AcceleroZ <- (df$Value.S.AcceleroZ - 512.0) / 256.0
  
  df <- cbind(df, jose_preproc_rain_sensor(df$Value.S.Rain))
  df$Value.S.Rain <- NULL
  
  if ("Value.S.CO2" %in% names(df))
    df$Value.S.CO2 <- df$Value.S.CO2 / 1000.0 # ppb
  if ("Value.S.COResistance" %in% names(df))
    df$Value.S.COResistance <- df$Value.S.COResistance / 1000.0
  if ("Value.S.No2Resistance" %in% names(df))
    df$Value.S.No2Resistance <- df$Value.S.No2Resistance / 1000.0
  if ("Value.S.O3Resistance" %in% names(df))
    df$Value.S.O3Resistance <- df$Value.S.O3Resistance / 1000.0
  
  df <- cbind(df, jose_preproc_sat_info(df$Value.S.SatInfo))
  df$Value.S.SatInfo <- NULL
  
  df$Value.S.Latitude <- jose_preproc_gps(df$Value.S.Latitude)
  df$Value.S.Longitude <- jose_preproc_gps(df$Value.S.Longitude)
  
  df <- df[, -grep("Audio", names(df))]
  
  names(df) <- tolower(gsub("^Value.", "", names(df)))
  df <- rename(
    df,
    c(
      "p.unitserialnumber" = "p.unit.serial.number",
      "p.18" = "p.unknown.18",
      "p.17" = "p.unknown.17",
      "p.19" = "p.unknown.19",
      "s.rgbcolor" = "s.rgb.color",
      "s.lightsensorblue" = "s.light.sensor.blue",
      "s.lightsensorgreen" = "s.light.sensor.green",
      "s.lightsensorred" = "s.light.sensor.red",
      "s.acceleroz" = "s.accelero.z",
      "s.acceleroy" = "s.accelero.y",
      "s.accelerox" = "s.accelero.x",
      "s.lightsensorbottom" = "s.light.sensor.bottom",
      "s.lightsensortop" = "s.light.sensor.top",
      "s.temperatureambient" = "s.temperature.ambient",
      "s.temperatureunit" = "s.temperature.unit",
      "s.secondofday" = "s.second.of.day",
      "p.totaluptime" = "p.total.up.time",
      "p.sessionuptime" = "p.session.up.time",
      "p.basetimer" = "p.base.timer"
    )
  )
  
  df <- df[, order(names(df))]
  
  return(df)
}

preproc_jose_types <- function(df) {
  df$s.satinfo.fix <-
    factor(
      df$s.satinfo.fix,
      levels = c("0", "1", "2", "3"),
      labels = c("No GPS", "No fix", "2D fix", "3D fix")
    )
  df$p.no2.heater.mode <-
    factor(df$p.no2.heater.mode,
           levels = c("0", "256", "2048", "2034", "2560", "2816"))
  df$p.co.heater.mode <-
    factor(
      df$p.co.heater.mode,
      levels = c("0", "256", "2048", "2034", "2560", "2816"),
      labels = c(
        "Manual mode - switched off",
        "Manual mode - switched on",
        "Automatic mode - finished cooling",
        "Automatic mode - finished heating",
        "Automatic mode - busy cooling",
        "Automatic mode - busy heating"
      )
    )
  return(df)
}

preproc_jose_bad_values <-
  function(df,
           max.dilution = 1,
           max.co2.ppm = 10000,
           max.no2.resistance = 2000,
           min.temp = -40,
           max.temp = 100,
           max.barometer = 1100,
           min.date = "2016-02-01", 
           max.date = "2999-01-01") {
    # p.error.booting
    # p.power.error
    # p.co.heater.mode        <> s.coresistance   = nothing
    # p.power.co2.sensor.on   <> s.co2            = real high (> 5000 ppm) and low (0)
    # p.power.co.heater.on    <> s.coresistance   = nothing
    # p.power.error           <> ?
    # p.power.h2s.sensor.on   <> ...
    # p.power.nh3.sensor.on   <> ...
    # p.power.no2.heater.on   <> s.no2resistance  = to high (> 1000 ppb) and low (< 50)
    # p.power.03.heater.on    <> s.o3resistance   = to high (> 60 kOhm)
    # p.power.pm.sensor.on    <> ?
    # s.satinfo.num           <> s.lat/long-itude = nothing
    # s.satinfo.dillution     <> s.lat/long-itude = nothing
    
    ## Data before 10 feb ------------------------------------------------------
    good_date <- df$datetime > strptime(min.date, format = "%Y-%m-%d") &
      df$datetime < strptime(max.date, format = "%Y-%m-%d")
    df <- df[good_date, ]
    
    # GPS -----------------------------------------------------------------------
    low_lat_long <- df$s.latitude == 0 | df$s.longitude == 0
    high_dilution <- df$s.satinfo.dilution > max.dilution
    df$s.latitude[low_lat_long | high_dilution] <- NA
    df$s.longitude[low_lat_long | high_dilution] <- NA
    
    ## CO2 ----------------------------------------------------------------------
    high_co2 <- df$s.co2 > max.co2.ppm
    df$s.co2[high_co2] <- NA
    
    ## NO2 ---------------------------------------------------------------------
    high_no2 <- df$s.no2resistance > max.no2.resistance
    df$s.no2resistance[high_no2] <- NA
    
    ## Temperature --------------------------------------------------------------
    low_temp <- df$s.temperature.unit < min.temp
    high_temp <- df$s.temperature.unit > max.temp
    df$s.temperature.unit[low_temp | high_temp] <- NA
    low_temp <- df$s.temperature.ambient < min.temp
    high_temp <- df$s.temperature.ambient > max.temp
    df$s.temperature.ambient[low_temp | high_temp] <- NA
    
    ## Pressure ----------------------------------------------------------------
    high_pressure <- df$s.barometer > max.barometer
    df$s.barometer[high_pressure] <- NA
    
    ## Remove s.10 col
    df$s.10 <- NULL
    
    return(df)
  }

f_to_bits <- function(x) {
  return(as.integer(intToBits(x)))
}

jose_preproc_power_state <- function(power) {
  power <- data.frame(t(sapply(power, f_to_bits)))
  power <- power[, -(16:32)]
  power$p.power.error <-
    as.integer(array(!power[, 1] & !power[, 2]))
  power$p.power.charged <- as.integer(array(!power[, 1] & power[2]))
  power$p.power.charging <-
    as.integer(array(power[, 1] & !power[, 2]))
  power$p.power.no.battery <-
    as.integer(array(power[, 1] & power[, 2]))
  power <- power[, -(1:2)]
  power <- rename(
    power,
    c(
      "X3" = "p.power.gauge.ok",
      "X4" = "p.power.energy.harvesting.standby",
      "X5" = "p.power.aux_power.input.active",
      "X6" = "p.power.harvest.input.active",
      "X7" = "p.power.usb.input.active",
      "X8" = "p.power.mains.input.active",
      "X9" = "p.power.co.heater.on",
      "X10" = "p.power.no2.heater.on",
      "X11" = "p.power.o3.heater.on",
      "X12" = "p.power.co2.sensor.on",
      "X13" = "p.power.h2s.sensor.on",
      "X14" = "p.power.nh3.sensor.on",
      "X15" = "p.power.pm.sensor.on"
    )
  )
  return(power)
}

jose_preproc_error_state <- function(error) {
  error <- data.frame(t(sapply(error, f_to_bits)))
  error <- error[, -(4:29)]
  error <- rename(
    error,
    c(
      "X1" = "p.error.wifi.connection",
      "X2" = "p.error.memory",
      "X3" = "p.error.configuration",
      "X30" = "p.error.sensor",
      "X31" = "p.error.base.irq.service.stopped",
      "X32" = "p.error.booting"
    )
  )
  return(error)
}

jose_preproc_split_mode <- function(mode, prefix) {
  col_mode <- paste(prefix, "mode", sep = ".")
  col_value <- paste(prefix, "value", sep = ".")
  mode <- data.frame(t(sapply(mode, f_to_bits)))
  a <- array(as.matrix(mode[, 1:16]) %*% as.matrix(2 ^ seq(0, 15)))
  mode[col_value] <- a
  mode[col_mode] <-
    array(as.matrix(mode[, 17:32]) %*% as.matrix(2 ^ seq(0, 15)))
  mode[col_mode] <- as.character(mode[, col_mode])
  mode <- mode[, -(1:32)]
  return(mode)
}

jose_preproc_rain_sensor <- function(rain) {
  rain <- data.frame(t(sapply(rain, f_to_bits)))
  rain <- rename(
    rain,
    c(
      "X1" = "s.rain.backside.left",
      "X2" = "s.rain.frontside.left",
      "X3" = "s.rain.frontside.right",
      "X4" = "s.rain.backside.right"
    )
  )
  rain <- rain[, -(5:32)]
  return(rain)
}

jose_preproc_sat_info <- function(satinfo) {
  satinfo <- data.frame(t(sapply(satinfo, f_to_bits)))
  bits8 <- as.matrix(2 ^ seq(0, 7))
  bits4 <- as.matrix(2 ^ seq(0, 3))
  satinfo$s.satinfo.num <-
    array(as.matrix(satinfo[, 1:8]) %*% bits8)
  satinfo$s.satinfo.fix <-
    array(as.matrix(satinfo[, 9:12]) %*% bits4)
  satinfo$s.satinfo.fix <-
    as.character(satinfo$s.satinfo.fix)
  satinfo$s.satinfo.dilution <-
    array(as.matrix(satinfo[, 17:24]) %*% bits8 +
            as.matrix(satinfo[, 13:16]) %*% bits4) / 10
  satinfo <- satinfo[, -(1:32)]
  return(satinfo)
}

jose_preproc_gps <- function(gps) {
  gps <- data.frame(t(sapply(gps, f_to_bits)))
  bits8 <- as.matrix(2 ^ seq(0, 7))
  bits20 <- as.matrix(2 ^ seq(0, 19))
  degrees <- array(as.matrix(gps[, 21:28]) %*% bits8 +
                     as.matrix(gps[, 1:20]) %*% bits20 / 2 ^ 20)
  # gps$gps.hemisphere <- as.character(gps[,32]), labels = c("0" = "North",
  # "1" = "South")
  return(degrees)
}