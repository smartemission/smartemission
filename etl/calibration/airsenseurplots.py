from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import requests
import json

ASE_DEFS = {
    '11820001': 'ASE_NL01',
    '11820002': 'ASE_NL02',
    '11820003': 'ASE_NL03',
    '11820004': 'ASE_NL04',
    '11820005': 'ASE_NL05',
}

GAS_DEFS = {
    'co': 'carbon_monoxide__air_',
    'no': 'nitrogen_monoxide__air_',
    'no2': 'nitrogen_dioxide__air_',
    'o3': 'ozone__air_',
}

SITE_DEFS = {
    'breuk-sw': 'breukelen_snelweg',
    'nijm-ruy': 'nijmegen_ruyterstraat',
}

# InfluxDB creds
INFLUX_DB_URL = 'https://test.smartemission.nl/influxdb/query?pretty=true'
INFLUX_DB = 'smartemission'
INFLUX_DB_READ_USER = 'smart'
INFLUX_DB_READ_PW = 'smart'
MEAS_RIVM = 'rivm'
MEAS_ASE = 'joserefined'


# Get calibrated or reference data from InfluxDB
def get_data(db, measurement, component, station, time_start, time_end):
    q = "SELECT time,component,station,value from %s WHERE time >= '%s' AND time <= '%s' AND station = '%s' AND component = '%s'" % (measurement, time_start, time_end, station, component)
    payload = {'q': q, 'db': db}
    auth = (INFLUX_DB_READ_USER, INFLUX_DB_READ_PW)

    # Remote Influx DB query
    r = requests.get(INFLUX_DB_URL, auth=auth, params=payload)
    json_data = json.loads(r.text)

    values_arr = None
    try:
        values_arr = json_data['results'][0]['series'][0]['values']
    except:
        pass

    # We need values hashtable indexed by datetime for later skipping
    values_dict = {}
    for value in values_arr:
        values_dict[value[0]] = value
    return values_arr, values_dict


# Make regression plots for specific date-period, a site, ASE stations, and gasses
def make_plots(date_start, date_end, site, ase_stations, gasses):

    # Go through all gasses and then for each gas RIVM and all AirSensEUR stations
    for gas in gasses:

        # Time formatting: complete ISO Datetime
        time_start = '%sT%sZ' % (date_start, '00:00:00')
        time_end = '%sT%sZ' % (date_end, '00:00:00')

        # Get RIVM (reference) ASE data from InfluxDB
        rivm_val_arr, rivm_val_dict = get_data(INFLUX_DB, MEAS_RIVM, GAS_DEFS[gas], SITE_DEFS[site], time_start, time_end)

        for ase in ase_stations:
            # Get calibrated (calculated) ASE data from InfluxDB
            se_val_arr, se_val_dict = get_data(INFLUX_DB, MEAS_ASE, gas, ase, time_start, time_end)

            x, y = [], []
            for se_val in se_val_arr:
                try:
                    # only use entries where for both hour-values exist, otherwise skip
                    rivm_val = rivm_val_dict[se_val[0]]
                except:
                    # No RIVM value for this hour, skip
                    continue

                y.append(se_val[3])
                rivm_val_g = rivm_val[3]
                if gas == 'co':
                    # RIVM has CO in mg/m3 so convert to ug/m3
                    rivm_val_g *= 1000.0
                x.append(rivm_val_g)

            # Make a Pandas Dataframe from the x and y single-dim arrays
            d = {'x': x, 'y': y}
            df = pd.DataFrame(data=d)

            # R-square calculator from the two x (Ref) and y (ASE) arrays
            def linregress(x, y):
                # Alternative R2 calc, leads to same value
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                r2 = r_value ** 2.0
                # r2 = stats.pearsonr(x, y)[0] ** 2.0
                return r2, slope

            # R-square calculator from the two x (Ref) and y (ASE) arrays
            def r_squared(x, y):
                r2, slope = linregress(x, y)
                return r2

            # Plot styling
            sns.set(rc={'axes.grid': True, 'grid.linestyle': '-', "axes.titlesize": 9, "axes.labelsize": 9, 'grid.color': '.8', 'patch.edgecolor': 'w', "xtick.major.size": 4, "ytick.major.size": 4})
            sns.set(font_scale=0.8)

            # Draw the plot
            # sns.lmplot(x='x', y='y', data=df)
            # sns.scatterplot(x="x", y="y", data=df)
            g = sns.PairGrid(df, y_vars=["y"], x_vars=["x"], height=5)
            g.map(sns.scatterplot, s=50)
            # g.set(ylim=(0,120), yticks=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90,100,110,120])

            # More styling
            r2, slope = linregress(x, y)

            plt.title("%s - %s - %s - %s to %s - R2=%.3f m=%.2f" % (gas.upper(), site, ASE_DEFS[ase], date_start, date_end, r2, slope))
            plt.xlabel('RIVM Ref (SOS) - 1h avg - ug/m3')
            plt.ylabel('ASE Calc - 1h avg - ug/m3')
            # plt.show()

            # Save to png file
            plt.savefig('airsenseur/%s-%s-%s-%s-%s.png' % (site, gas, ASE_DEFS[ase], date_start, date_end))
            plt.close()


if __name__ == '__main__':
    make_plots('2018-09-10', '2018-10-09', 'breuk-sw', ASE_DEFS.keys(), ['no', 'no2', 'o3'])
    make_plots('2018-12-25', '2019-01-24', 'nijm-ruy', ['11820001'], ['co', 'no', 'no2', 'o3'])
