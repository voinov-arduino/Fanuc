from pycomm3 import LogixDriver

if __name__ == '__main__':
    plc = LogixDriver('192.168.0.101')
    with plc:
        # print(plc.get_tag_list(program='*'))
        print(plc.read('SINT'))

    # plc.open( direct_connection=True)
    # print(plc.tags)
