from numpy import linspace

# Preparation
sample_ratio = 1/45.0

# Modeling
n_iter = 2
cv_k = 10

# Visualization
n_interp = 100
effect_plots = {'s.barometer': linspace(970, 1040, n_interp),
                's.co2': linspace(0, 1400, n_interp),
                's.humidity': linspace(20, 110, n_interp),
                's.no2resistance': linspace(0, 2000, n_interp),
                's.o3resistance': linspace(0, 500, n_interp),
                's.temperature.ambient': linspace(-5, 40, 100, n_interp),
                's.temperature.unit': linspace(0, 60, 100, n_interp)}
ax_limits = {'O3_Waarden': (-10, 220),
             'CO_Waarden': (-10, 1200),
             'NO2_Waarden': (-20, 80)}
res_limits = {'O3_Waarden': (-30, 30),
              'CO_Waarden': (-300, 300),
              'NO2_Waarden': (-30, 30)}

# Process
verbose = 3
n_jobs = -1