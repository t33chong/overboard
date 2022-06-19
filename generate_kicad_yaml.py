# Used with https://github.com/mcbridejc/kicad_component_layout

import yaml

SWITCH_INTERVAL = 19.05

LED_ORDER = """
00 07 10 17 20 27
30 37 40 47 50 57
56 51 46 41 36 31
26 21 16 11 06 01
02 05 12 15 22 25
32 35 42 45 52 55
54 53 44 43 34 33
24 23 14 13 04 03
"""

ROT_ORDER = """
0 0 0 0 0 0
0 0 0 0 0 0
1 1 1 1 1 1
1 1 1 1 1 1
0 0 0 0 0 0
0 0 0 0 0 0
1 1 1 1 1 1
1 1 1 1 1 1
"""


COLUMNS = '012345ABCDEF'
RGB_MATRIX = """
43 44 45 46 47 48 01 02 03 04 05 06
42 41 40 39 38 37 12 11 10 09 08 07
31 32 33 34 35 36 13 14 15 16 17 18
30 29 28 27 26 25 24 23 22 21 20 19
"""
rgb_matrix = []
for line in RGB_MATRIX.split('\n'):
    line = line.strip()
    if not line:
        continue
    rgb_matrix.append(line.split(' '))
print(rgb_matrix)

components = {}

def align_component(x, y, rotation=0, flipped=False):
    return {
        'location': [x, y],
        'rotation': rotation,
        'flip': flipped
    }

# Switches
def add_switch(c, r, x, y, rotation):
    components['K{}{}'.format(c, r)] = align_component(x, y, rotation)

    # THT Diode
    diode_x = x
    diode_y = y + SWITCH_INTERVAL * 1/2
    diode_rot = 180
    # components['D{}{}'.format(c, r)] = align_component(diode_x, diode_y, diode_rot, True)

# RGB LEDs
def add_rgb(rgb_id, x, y, rotation):
    if rgb_id.startswith('0'):
        rgb_id = rgb_id[-1]
    components[f'RGB{rgb_id}'] = align_component(x, y, rotation, True)

# Diodes
def add_diode(c, r, x, y, rotation):
    components['D{}{}'.format(c, r)] = align_component(x, y, rotation, True)

k00_offset_x = -125.720075
k00_offset_y = -32.9363
col_x_interval = 18.908
col_y_interval = 2.322
row_x_interval = -2.322
row_y_interval = 18.908

# 5.08mm rotated
rgb_offset_x = 0.619
rgb_offset_y = 5.042

# (19.05/2)mm rotated
diode_offset_x = 1.161
diode_offset_y = 9.454

x = k00_offset_x
y = k00_offset_y
for c in range(6):
    switch_x = x
    switch_y = y
    for r in range(4):
        add_switch(COLUMNS[c], r, switch_x, switch_y, 180-7)
        add_diode(COLUMNS[c], r, switch_x + diode_offset_x, switch_y - diode_offset_y, 180-7)
        add_rgb(rgb_matrix[r][c], switch_x + rgb_offset_x, switch_y - rgb_offset_y, 180-7)
        # add from KF0 (x inverse of K00 because it's distance from origin, y same) in reverse
        # row increments the same, y remains the same
        # col decrements from F, x is -x
        add_switch(COLUMNS[11-c], r, -switch_x, switch_y, 180+7)
        add_diode(COLUMNS[11-c], r, -switch_x - diode_offset_x, switch_y - diode_offset_y, 180+7)
        add_rgb(rgb_matrix[r][11-c], -switch_x - rgb_offset_x, switch_y - rgb_offset_y, 180+7)
        switch_x += row_x_interval
        switch_y += row_y_interval
    x += col_x_interval
    y += col_y_interval

add_switch(9, 2, 0 - 18.68, SWITCH_INTERVAL * 2, 180)
add_switch(9, 3, 0, SWITCH_INTERVAL * 2, 180)
add_switch(9, 4, 0 + 18.68, SWITCH_INTERVAL * 2, 180)

# LEDs
def add_led(led_id, switch_id, rotation_code):
    x, y = components['K{}'.format(switch_id)]['location']
    rotation = int(rotation_code) * 180
    # Average of MX, TTC LP, Choc v1 & v2
    # components['LED{}'.format(led_id)] = align_component(x, y - 4.9625, rotation, True)
    components['LED{}'.format(str(led_id).zfill(2))] = align_component(x, y - 5, rotation, True)

# for lid, sid, rc in zip(range(48), LED_ORDER.strip().split(), ROT_ORDER.strip().split()):
#     add_led(lid, sid, rc)

# YAML dump
pcb_data = {
    'origin': [0, 0],
    'components': components
}

with open('layout.yaml', 'w') as f:
    f.write(yaml.dump(pcb_data))
