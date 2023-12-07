from client.entity import Drive
from eclipse_request import EclipseRequest


def main():

    drv = Drive(nas_id=1, delivery_id=2)

    ereq = EclipseRequest("POST", drv, url_params=None)
    ereq.send()


if __name__ == "__main__":
    main()


