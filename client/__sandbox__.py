from client.entity import Drive, Nasbox
from client.copy import EclipseCopy
from eclipse_request import EclipseRequest


def main():

    nb = Nasbox()

    ereq = EclipseRequest("GET", nb, url_params=None)
    res = ereq.send()
    print()


if __name__ == "__main__":
    main()


