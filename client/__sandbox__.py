from client.entity import Nasbox
from eclipse_request import EclipseRequest
from client.copy import EclipseCopy, KISIK_TO_GEOBC

# --
DELIVERY_ID = 1

# ROOT for SRC and DST
SANDBOX = r"/home/jordan/work/geobc/sandbox"

# test source dir
DRIVE = r"/drive"
SRC = SANDBOX + DRIVE

# test dst dir
SHARED_FOLDER = r"/shared_folder"
DST = SANDBOX + SHARED_FOLDER


def main():

    nb = Nasbox.create("")
    ereq = EclipseRequest("GET", nb, url_params=None)
    res = ereq.send()
    nas_tgt = res[1]
    ipv4_addr = nas_tgt["ipv4_addr"]

    src = SRC
    dst = "/mnt/nfs_server"

    nas_id = nas_tgt['id']
    delivery_id = DELIVERY_ID

    ecopy = EclipseCopy(
        src=src, dst=dst, nas_id=nas_id, delivery_id=delivery_id, folder_mapping=KISIK_TO_GEOBC
    )

    ecopy.copy()


if __name__ == "__main__":
    main()


