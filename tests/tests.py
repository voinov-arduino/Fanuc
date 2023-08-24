if __name__ == '__main__':
    elements = [(929, 570), (65477, 64917), (165, 901), (0, 257), (0, 64893), (65531, 65117)]
    new_elements = []
    for elem in elements:
        print(elem)
        new_elem = ""
        first = str(elem[0])
        second = str(elem[1])
        if elem[0] > (65356 / 2):
            print(elem[0], elem[0] - 65356)
            first = str(elem[0] - 65356)
        if elem[1] > (65356 / 2):
            print(elem[1] - 65356)
            second = str(elem[1] - 65356)
        new_elem = float(f"{first}.{second}")
        new_elements.append(new_elem)
    print(
        f'X: {new_elements[0]}, Y: {new_elements[1]}, Z: {new_elements[2]}, W: {new_elements[3]}, P: {new_elements[4]}, R: {new_elements[5]}')
