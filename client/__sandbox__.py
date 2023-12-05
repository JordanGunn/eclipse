from client.entity import Drive
from eclipse_request import EclipseRequest


def main():
    drv = Drive(1, 2)

    ereq = EclipseRequest("POST", drv, url_params=None)
    print()


if __name__ == "__main__":
    main()


