import subprocess
import os


def make_tp(filename, directory):
    with open(fr"{directory}\robot.ini", "w") as robot_ini:
        lines = [
            "[WinOLPC_Util]\n",
            "Robot=\\C\\Users\\02Robot\\Documents\\My Workcells\\Fanuc_002\\Robot_1\n",
            "Version=V7.70-1\n",
            "Path=C:\\Program Files (x86)\\FANUC\\WinOLPC\\Versions\\V770-1\\bin\n",
            "Support=C:\\Users\\02Robot\\Documents\\My Workcells\\Fanuc_002\\Robot_1\\support\n",
            "Output=C:\\Users\\02Robot\\Documents\\My Workcells\\Fanuc_002\\Robot_1\\output"
        ]
        robot_ini.writelines(lines)
    out = subprocess.check_output(['maketp', filename], cwd=directory)
    if out:
        out = out.decode('utf-8').strip().split("\n")
    else:
        out = []

    return is_tp_file_exist(filename, directory), out


def is_tp_file_exist(ls_filename: str, directory) -> bool:
    index_of_point = ls_filename.find(".")
    if index_of_point != -1:
        tp_filename = f"{ls_filename[:index_of_point]}.tp"
    else:
        tp_filename = f"{ls_filename}.tp"
    return os.path.exists(fr"{directory}\{tp_filename}")


if __name__ == '__main__':
    make_tp('fr"{directory}\robot.ini"', r"tests")
