def delete_approximate(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        modified_lines = [line for line in lines if ": Weave Sine[10];" not in line and ": Weave End[10];" not in line]

        new_file_name = file_name.replace('.', '_NoApproximated.')
        with open(new_file_name, 'w') as new_file:
            new_file.writelines(modified_lines)
        print(new_file_name)
    except FileNotFoundError:
        print(f"File {file_name} not exist")
    except Exception as e:
        print(f"Error: {e}")


delete_approximate("layer_40.ls")
