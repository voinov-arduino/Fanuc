import re

input_filename = 'layer_40.ls'
output_filename = f'{input_filename[:-3]}_Cords_Lidar.ls'

with open(input_filename, "r") as input_file:
    sample_lines = input_file.readlines()

coordinate_pattern = re.compile(r'X = ([-+]?\d*\.\d+) mm, Y = ([-+]?\d*\.\d+) mm, Z = ([-+]?\d*\.\d+) mm')

previous_x, previous_y = None, None
i = 1
with open(output_filename, "w") as output_file:
    for line in sample_lines:
        match = coordinate_pattern.search(line)
        if match and i != 1:
            x, y, z = float(match.group(1)), float(match.group(2)), float(match.group(3))
            if previous_x is not None and previous_y is not None and previous_z is not None:
                middle_x = (x + previous_x) / 2
                middle_y = (y + previous_y) / 2
                z += 150
                output_line = f'\t   X = {middle_x:.3f} mm, Y = {middle_y:.3f} mm, Z = {z:.3f} mm\n'
                print(i, output_line)
                i += 1
                output_file.write(output_line)
            previous_x, previous_y, previous_z = x, y, z
        else:
            output_file.write(line)
            i += 1
