from client.entity import _Nasbox
from eclipse_request import EclipseRequest
from client.copy import EclipseCopy, KISIK_TO_GEOBC

DELIVERY_ID = 1
COPY_SRC = r"/home/jordan/work/geobc/sandbox/drive"


def main():

    # nb = Nasbox()
    # ereq = EclipseRequest("GET", nb, url_params=None)
    # res = ereq.send()
    # nas_tgt = res[1]
    #
    # src = COPY_SRC
    # dst = "/home/jordan/work/geobc/sandbox/nasbox"
    #
    # nas_id = nas_tgt['id']
    # delivery_id = DELIVERY_ID
    #
    # ecopy = EclipseCopy(
    #     src=src, dst=dst, nas_id=nas_id, delivery_id=delivery_id, folder_mapping=KISIK_TO_GEOBC
    # )
    #
    # ecopy.copy()

    nb = _Nasbox.create("127.0.0.1:/home/jordan/shared_folder")
    print(nb.path)



if __name__ == "__main__":
    main()


