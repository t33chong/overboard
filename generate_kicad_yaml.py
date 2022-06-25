# Used with https://github.com/mcbridejc/kicad_component_layout

import yaml

SWITCH_INTERVAL = 19.05

# LED_ORDER = """
# 00 07 10 17 20 27
# 30 37 40 47 50 57
# 56 51 46 41 36 31
# 26 21 16 11 06 01
# 02 05 12 15 22 25
# 32 35 42 45 52 55
# 54 53 44 43 34 33
# 24 23 14 13 04 03
# """

# ROT_ORDER = """
# 0 0 0 0 0 0
# 0 0 0 0 0 0
# 1 1 1 1 1 1
# 1 1 1 1 1 1
# 0 0 0 0 0 0
# 0 0 0 0 0 0
# 1 1 1 1 1 1
# 1 1 1 1 1 1
# """


COLUMNS = '012345ABCDEF'
# RGB_MATRIX = """
# 43 44 45 46 47 48 01 02 03 04 05 06
# 42 41 40 39 38 37 12 11 10 09 08 07
# 31 32 33 34 35 36 13 14 15 16 17 18
# 30 29 28 27 26 25 24 23 22 21 20 19
# """
RGB_MATRIX = """
06 05 04 03 02 01 48 47 46 45 44 43
07 08 09 10 11 12 37 38 39 40 41 42
18 17 16 15 14 13 36 35 34 33 32 31
19 20 21 22 23 24 25 26 27 28 29 30
"""
RGB_ROTATION = """
1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0
"""
rgb_matrix = []
for line in RGB_MATRIX.split('\n'):
    line = line.strip()
    if not line:
        continue
    rgb_matrix.append(line.split(' '))
print(rgb_matrix)
rgb_rotation = []
for line in RGB_ROTATION.split('\n'):
    line = line.strip()
    if not line:
        continue
    rgb_rotation.append(list(int(n) * 180 for n in line.split(' ')))
print(rgb_rotation)

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

# LEDs
def add_led(led_id, x, y):
    components[f'LED{led_id}'] = align_component(x, y)

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
led_offset_x = 0.619
led_offset_y = 5.042

# (19.05/2)mm rotated
# diode_offset_x = 1.161
# diode_offset_y = 9.454
diode_offset_x = 1.006
diode_offset_y = 8.194

x = k00_offset_x
y = k00_offset_y
for c in range(6):
    switch_x = x
    switch_y = y
    for r in range(4):
        add_switch(COLUMNS[c], r, switch_x, switch_y, -7)
        # add_diode(COLUMNS[c], r, switch_x + diode_offset_x, switch_y - diode_offset_y, 180-7)
        # add_diode(COLUMNS[c], r, switch_x + diode_offset_y, switch_y + diode_offset_x, 90-7)
        add_diode(COLUMNS[c], r, switch_x - diode_offset_x, switch_y + diode_offset_y, 180-7)
        add_rgb(rgb_matrix[r][c], switch_x + led_offset_x, switch_y - led_offset_y, rgb_rotation[r][c]-7)
        # add from KF0 (x inverse of K00 because it's distance from origin, y same) in reverse
        # row increments the same, y remains the same
        # col decrements from F, x is -x
        add_switch(COLUMNS[11-c], r, -switch_x, switch_y, 7)
        # add_diode(COLUMNS[11-c], r, -switch_x - diode_offset_x, switch_y - diode_offset_y, 180+7)
        # add_diode(COLUMNS[11-c], r, -switch_x - diode_offset_y, switch_y + diode_offset_x, 90+7)
        add_diode(COLUMNS[11-c], r, -switch_x + diode_offset_x, switch_y + diode_offset_y, 180+7)
        add_rgb(rgb_matrix[r][11-c], -switch_x - led_offset_x, switch_y - led_offset_y, rgb_rotation[r][11-c]+7)
        switch_x += row_x_interval
        switch_y += row_y_interval
    x += col_x_interval
    y += col_y_interval

# add_diode(
#     1, 3,
#     components['K13']['location'][0] + 9.454, components['K13']['location'][1] + 1.161, 270-7)
# add_diode(
#     'E', 3,
#     components['KE3']['location'][0] - 9.454, components['K13']['location'][1] + 1.161, 270+7)
def move_diode(refnum_string, direction):
    col = refnum_string[0]
    row = refnum_string[1]
    if col.isalpha():
        rotation = 7
    else:
        rotation = -7
    vertical = direction[0]
    horizontal = direction[1]
    if vertical == 'N':
        y = components[f'K{refnum_string}']['location'][1] - diode_offset_x
    else:  # S
        y = components[f'K{refnum_string}']['location'][1] + diode_offset_x
    if horizontal == 'W':
        x = components[f'K{refnum_string}']['location'][0] - diode_offset_y
    else:  # E
        x = components[f'K{refnum_string}']['location'][0] + diode_offset_y
    add_diode(col, row, x, y, 270 + rotation)
move_diode('03', 'SE')
move_diode('13', 'NW')
move_diode('23', 'SE')
move_diode('33', 'SE')
move_diode('C3', 'SW')
move_diode('D3', 'SW')
move_diode('E3', 'NE')
move_diode('F3', 'SW')
move_diode('11', 'SE')

# add_diode(
#     1, 3,
#     components['K13']['location'][0] + diode_offset_y,
#     components['K13']['location'][1] + diode_offset_x,
#     270-7)
# add_diode(
#     'E', 3,
#     components['KE3']['location'][0] - diode_offset_y,
#     components['KE3']['location'][1] + diode_offset_x,
#     270+7)

add_switch(9, 2, -18.68, SWITCH_INTERVAL * 2, 180)
add_led(1, -18.68, SWITCH_INTERVAL * 2 - 5.08)
add_switch(9, 3, 0, SWITCH_INTERVAL * 2, 180)
add_led(2, 0, SWITCH_INTERVAL * 2 - 5.08)
add_switch(9, 4, 18.68, SWITCH_INTERVAL * 2, 180)
add_led(3, 18.68, SWITCH_INTERVAL * 2 - 5.08)

# LEDs
def add_led(led_id, switch_id, rotation_code):
    x, y = components['K{}'.format(switch_id)]['location']
    rotation = int(rotation_code) * 180
    # Average of MX, TTC LP, Choc v1 & v2
    # components['LED{}'.format(led_id)] = align_component(x, y - 4.9625, rotation, True)
    components['LED{}'.format(str(led_id).zfill(2))] = align_component(x, y - 5, rotation, True)

# for lid, sid, rc in zip(range(48), LED_ORDER.strip().split(), ROT_ORDER.strip().split()):
#     add_led(lid, sid, rc)

# OLED
components['OLED1'] = align_component(0, -33.2)

# TrackPoint mounting holes
components['H1'] = align_component(0, 2.595001)

# Pin headers adjoining boards
components['J4'] = align_component(-138.509375, -22.225)
components['J5'] = align_component(138.509375, -22.225)

# Encoders
components['ENC1'] = align_component(-11.90625, 19)
components['ENC2'] = align_component(11.90625, 19)

# YAML dump
pcb_data = {
    'origin': [0, 0],
    'components': components
}

with open('layout.yaml', 'w') as f:
    f.write(yaml.dump(pcb_data))
