import cpppo

from cpppo.server.enip import client
from cpppo.server.enip.get_attribute import attribute_operations
from cpppo.server.enip.get_attribute import proxy_simple

if __name__ == '__main__':
    HOST = "192.168.0.101"
    TAGS = ["@4/100/0"]

    with client.connector(host=HOST) as conn:
        for index, descr, op, reply, status, value in conn.synchronous(
                operations=attribute_operations(
                    TAGS, route_path=[], send_path='')):
            print(value)


    data, = proxy_simple("192.168.0.101").read([('@4/100/0', 'SINT')])
    print(data)