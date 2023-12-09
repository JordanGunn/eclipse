from client.entity import Drive
from client.copy import EclipseCopy
from eclipse_request import EclipseRequest


def main():

    drv = Drive(nas_id=1, delivery_id=2)

    ereq = EclipseRequest("POST", drv, url_params=None)
    ereq.send()

    ecopy = EclipseCopy("src", "dst")
    ecopy.nas_id = 1
    ecopy.delivery_id = 1


if __name__ == "__main__":
    main()


