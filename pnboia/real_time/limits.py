range_limits = {
    "wvht": [0.1, 19.9],
    "wmax": [0.1, 19.9],
    "dpd": [1.7, 30],
    "mwd": [0, 360],
    "wspd1": [0.1, 59],
    "wdir1": [0, 360],
    "gust1": [0.1, 59],
    "wspd2": [0.1, 59],
    "wdir2": [0, 360],
    "gust2": [0.1, 59],
    "atmp": [-39, 59],
    "pres": [501, 1099],
    "dewp": [-29, 39],
    "wtmp": [-3, 39],
    "humi": [25, 102],
    "cvel1": [-4990, 4990],
    "cdir1": [0, 360],
    "cvel2": [-4990, 4990],
    "cdir2": [0, 360],
    "cvel3": [-4990, 4990],
    "cdir3": [0, 360],
    "apd": [1.7, 30],
    }

sigma_limits = {
    "wvht": 6,
    "humi": 20,
    "pres": 21,
    "atmp": 11,
    "wspd": 25,
    "wtmp": 8.6,
    }

mis_value_limits = {
    "humi": 11,
    "cvel1": 409.5,
    "cdir1": 511,
    "cvel2": 409.5,
    "cdir2": 511,
    "cvel3": 409.5,
    "cdir3": 511,
    "dewp": -10,
    "atmp": -10,
    "wtmp": 40.955,
    "wvht": 20.47,
    "wmax": 20.47,
    "dpd": 25.5,
    "mwd": 381,
    "spred": 381,
    }

climate_limits = {
    "wwht": [0, 15],
    "wmax": [0, 19],
    "dpd": [1.7, 20],
    "wspd1": [0, 59],
    "gust1": [0, 59],
    "wspd2": [0, 59],
    "gust2": [0, 59],
    "atmp": [-8, 42],
    "atmp": [8, 48],
    "atmp": [15, 48],
    "pres": [950, 1050],
    "dewp": [-29, 39],
    "wtmp": [-3, 39],
    "apd": [1.7, 20],
    "cvel1": [-2500, 2500],
    "cvel2": [-2500, 2500],
    "cvel3": [-2500, 2500],
    }


std_mean_values = {
    "wwht": [0, 15],
    "wmax": [0, 19],
    "dpd": [1.7, 20],
    "wspd1": [0, 59],
    "gust1": [0, 59],
    "wspd2": [0, 59],
    "gust2": [0, 59],
    "atmp": [-8, 42],
    "atmp": [8, 48],
    "atmp": [15, 48],
    "pres": [950, 1050],
    "dewp": [-29, 39],
    "wtmp": [-3, 39],
    "apd": [1.7, 20],
    "cvel1": [-2500, 2500],
    "cvel2": [-2500, 2500],
    "cvel3": [-2500, 2500],
    }

stuck_limits = 7

continuity_limits = 3
