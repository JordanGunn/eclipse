from client.entity import Nasbox
from eclipse_request import EclipseRequest
from eclipse_config import NetworkConfig
from client.copy import EclipseCopy, KISIK_TO_GEOBC

DELIVERY_ID = 1
COPY_SRC = r"/home/jordan/work/geobc/sandbox/drive"


def main():

    nb = Nasbox()
    ereq = EclipseRequest("GET", nb, url_params=None)
    res = ereq.send()
    nas_tgt = res[1]

    src = COPY_SRC
    dst = "/home/jordan/work/geobc/sandbox/nasbox"

    nas_id = nas_tgt['id']
    delivery_id = DELIVERY_ID

    ecopy = EclipseCopy(
        src_dir=src, dst_dir=dst, nas_id=nas_id, delivery_id=delivery_id, folder_mapping=KISIK_TO_GEOBC
    )

    port = NetworkConfig.PORT.DEFAULT
    ipv4_addr = nas_tgt["ipv4_addr"]

    ecopy.set_network_info(port=port, nas_location=ipv4_addr)
    ecopy.copy()


if __name__ == "__main__":
    main()


