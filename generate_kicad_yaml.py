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

k00_offset_x = -125.720075
k00_offset_y = -32.9363
col_x_interval = 18.908
col_y_interval = 2.322
row_x_interval = -2.322
row_y_interval = 18.908

x = k00_offset_x
y = k00_offset_y
for c in range(6):
    switch_x = x
    switch_y = y
    for r in range(4):
        add_switch(c, r, switch_x, switch_y, 180-7)
        # add from KF0 (x inverse of K00 because it's distance from origin, y same) in reverse
        # row increments the same, y remains the same
        # col decrements from F, x is -x
        add_switch('FEDCBA'[c], r, -switch_x, switch_y, 180+7)
        switch_x += row_x_interval
        switch_y += row_y_interval
    x += col_x_interval
    y += col_y_interval

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
