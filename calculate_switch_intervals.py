plate_width = 285.75015  # plate, not pcb - based on svg sent to sendcutsend
plate_height = 95.12060

center_x = plate_width / 2
center_y = plate_height / 2

k00_x1, k00_y1 = 10.155, 7.624  # top-left corner node of switch after -7deg rotation
k00_x2, k00_y2 = 24.155, 21.624  # bottom-right corner node of switch after -7deg rotation
k00_x = (k00_x1 + k00_x2) / 2  # absolute horizontal center of switch
k00_y = (k00_y1 + k00_y2) / 2  # absolute vertical center of switch

k00_offset_x = k00_x - center_x  # horizontal center of switch relative to the origin in the center of the board
k00_offset_y = k00_y - center_y  # vertical center of switch relative to the origin in the center of the board

# mock
k00_x1, k00_y1 = 22.439, -37.932

# calculate directional intervals between rows
# k01_x1, k01_y1 = 7.833, 26.526  # actual
k01_x1, k01_y1 = 20.117, -19.024  # mock
row_x_interval = k01_x1 - k00_x1
row_y_interval = k01_y1 - k00_y1

# calculate interval between columns
# k10_x1, k10_y1 = 29.063, 9.946  # actual
k10_x1, k10_y1 = 41.347, -35.610  # mock
col_x_interval = k10_x1 - k00_x1
col_y_interval = k10_y1 - k00_y1

print(f"""
k00_offset_x = {k00_offset_x}
k00_offset_y = {k00_offset_y}
col_x_interval = {col_x_interval}
col_y_interval = {col_y_interval}
row_x_interval = {row_x_interval}
row_y_interval = {row_y_interval}
""")
