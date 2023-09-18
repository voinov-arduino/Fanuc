import re
from scipy.stats import norm


def process_gcode_with_gaussian_density(input_filename):
    with open(input_filename, "r") as input_file:
        fanuc_lines = input_file.readlines()
    output_filename = f'{input_filename[:-3]}_Cords_Lidar_Gauss.ls'
    coordinate_pattern = re.compile(r'X = ([-+]?\d*\.\d+) mm, Y = ([-+]?\d*\.\d+) mm, Z = ([-+]?\d*\.\d+) mm')

    previous_x, previous_y, previous_z = None, None, None

    with open(output_filename, "w") as output_file:
        for line in fanuc_lines:
            match = coordinate_pattern.search(line)
            if match:
                x, y, z = float(match.group(1)), float(match.group(2)), float(match.group(3))
                if previous_x is not None and previous_y is not None and previous_z is not None:
                    middle_x = (x + previous_x) / 2
                    middle_y = (y + previous_y) / 2
                    sigma = 0.9
                    # Вычислите плотность вероятности
                    density_x = norm.pdf(x, middle_x, sigma)
                    density_y = norm.pdf(y, middle_y, sigma)

                    output_line = f'X = {density_x:.3f} mm, Y = {density_y:.3f} mm, Z = {z:.3f} mm,\n'
                    output_file.write(output_line)
                previous_x, previous_y, previous_z = x, y, z
            else:
                output_file.write(line)
