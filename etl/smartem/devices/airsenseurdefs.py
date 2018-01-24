from airsenseurfuncs import *

# All sensor definitions, both base sensors (AirSensEUR) and derived (virtual) sensors
# Carbon_monoxide = c("co_a4","CO-B4", "CO_MF_200", "CO_MF_20", "CO/MF-200", "CO3E300","co_mf_200"),
# Nitric_oxide = c("no_b4","no-b4_op1","NO-B4", "NO_C_25", "NO/C-25","NO3E100"))
# Nitrogen_dioxide = c("no2_b43f","NO2-B43F", "NO2_C_20", "NO2/C-20", "NO23E50"),
# Ozone = c("o3_a431","O3_M-5","O3/M-5", "O3-B4", "O33EF1","o3_m_5"),

# Names
# Geonovum1 ASE
# 'CO3E300', 'NO3E100', 'NO23E50',  'O33EF1'
# JustObjects1 ASE
# 'CO/MF-200', 'NO-B4', 'NO2-B43F' 'O3/M-5'
SENSOR_DEFS = {
    'CO3E300':
        {
            'label': 'CORaw',
            'vendor': 'CityTech',
            'meta': 'https://www.thebigredguide.com/docs/fullspec/co3e300.pdf',
            'unit': 'unknown',
            'meta_id': 'CO3E300',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'CO/MF-200':
        {
            'label': 'CORaw',
            'vendor': 'Membrapor',
            'meta': 'http://www.membrapor.ch/sheet/CO-MF-200.pdf',
            'unit': 'unknown',
            'meta_id': 'CO/MF-200',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'NO3E100':
        {
            'label': 'NORaw',
            'vendor': 'CityTech',
            'meta': 'http://www.gassensor.ru/data/files/nitric_oxide/no3e100.pdf',
            'unit': 'unknown',
            'meta_id': 'NO3E100',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'NO-B4':
        {
            'label': 'NORaw',
            'vendor': 'AlphaSense',
            'meta': 'http://www.alphasense.com/WEB1213/wp-content/uploads/2015/03/NO-B4.pdf',
            'unit': 'unknown',
            'meta_id': 'NO-B4',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'NO23E50':
        {
            'label': 'NO2Raw',
            'vendor': 'CityTech',
            'meta': 'http://www.gassensor.ru',
            'unit': 'unknown',
            'meta_id': 'NO23E50',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'NO2-B43F':
        {
            'label': 'NO2Raw',
            'vendor': 'AlphaSense',
            'meta': 'http://www.alphasense.com/WEB1213/wp-content/uploads/2017/07/NO2B43F.pdf',
            'unit': 'unknown',
            'meta_id': 'NO2-B43F',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'O33EF1':
        {
            'label': 'O3Raw',
            'vendor': 'CityTech',
            'meta': 'http://www.yousensing.com/UploadFiles/20081213232449907.pdf',
            'desc': 'must be O3 3E1F',
            'unit': 'unknown',
            'meta_id': 'O33EF1',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'O3/M-5':
        {
            'label': 'O3Raw',
            'vendor': 'AlphaSense',
            'meta': 'http://www.diltronic.com/wordpress/wp-content/uploads/O3-M-5.pdf',
            'unit': 'unknown',
            'meta_id': 'O3/M-5',
            'converter': convert_none,
            'type': int,
            'min': 10,
            'max': 150000
        },
    'Tempe':
        {
            'label': 'Temperatuur',
            'unit': 'Celsius',
            'min': -25,
            'max': 60
        },
    'Press':
        {
            'label': 'Luchtdruk',
            'unit': 'HectoPascal',
            'min': 200,
            'max': 1100

        },
    'Humid':
        {
            'label': 'Relative Humidity',
            'unit': '%RH',
            'min': 20,
            'max': 100
        },
    'temperature':
        {
            'label': 'Temperatuur',
            'unit': 'Celsius',
            'input': 'Tempe',
            'meta_id': 'ase-Tempe',
            'converter': convert_none,
            'type': int,
            'min': -25,
            'max': 60
        },
    'pressure':
        {
            'label': 'Luchtdruk',
            'unit': 'HectoPascal',
            'input': 'Press',
            'meta_id': 'ase-Press',
            'converter': convert_none,
            'type': int,
            'min': 200,
            'max': 1100
        },
    'humidity':
        {
            'label': 'Luchtvochtigheid',
            'unit': 'Procent',
            'input': 'Humid',
            'meta_id': 'ase-Humid',
            'converter': convert_none,
            'type': int,
            'min': 20,
            'max': 100
        },
    'coraw':
        {
            'label': 'CORaw',
            'unit': 'mVolt',
            'input': ['CO3E300', 'CO/MF-200'],
            'min': 10,
            'max': 150000,
            'converter': convert_none,
        },

    'noraw':
        {
            'label': 'NORaw',
            'unit': 'mVolt',
            'input': ['NO3E100', 'NO-B4'],
            'min': 10,
            'max': 150000,
            'converter': convert_none,
        },
    'no2raw':
        {
            'label': 'NO2Raw',
            'unit': 'mVolt',
            'input': ['NO23E50', 'NO2-B43F'],
            'min': 10,
            'max': 150000,
            'converter': convert_none,
        },
    'o3raw':
        {
            'label': 'O3Raw',
            'unit': 'mVolt',
            'input': ['O33EF1', 'O3/M-5'],
            'min': 10,
            'max': 150000,
            'converter': convert_none,
        }
}
