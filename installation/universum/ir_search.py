import os
import numpy as np

from espaces import espaces

NU_0 = 1.7e-5
SR = 44100
F_0 = 200

# # e3
# ir_params = {
#     'ev_params': {
#         'space': 'e3',
#         'F': 0.2 * np.array([F_0, F_0, F_0]),
#         'j_max': 101
#     },
#     'duration': 15,
#     'nu': 1e2 * NU_0,  # 2e2 * NU_0,
#     'sampling_rate': SR,
# }

# # s3
# ir_params = {
#     'ev_params': {
#         'space': 's3',
#         'F': 0.025 * np.array([F_0]),
#         'j_max': 5000
#     },
#     'duration': 60,
#     'nu': 1.5*1e2 * NU_0,
#     'sampling_rate': SR,
# }


# h2e1
ir_params = {
    'ev_params': {
        'space': 'h2e1',
        'F': 0.5 * np.array([F_0]),
        'j_max': 5000
    },
    'duration': 60,
    'nu': 1e3 * NU_0,
    'sampling_rate': SR,
}

# # s2e1
# ir_params = {
    # 'ev_params': {
    #     'space': 's2e1',
    #     'F': 0.5 * np.array([F_0, F_0]),
    #     'j_max': 5000
    # },
    # 'duration': 60,
    # 'nu': 1.5*1e2 * NU_0,
    # 'sampling_rate': SR,
# }

print ir_params
paths = espaces(ir_params)

# os.system("open %s" % os.path.split(paths['audio'])[0])
# os.system("open %s" % paths['audio'])
os.system("open %s" % paths['image'])
