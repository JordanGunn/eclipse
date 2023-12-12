class MissingFkError(Exception):
    """Exception indicating that EclipseCopy is missing the delivery id foreign key."""

    def __init__(self, message="Missing foreign keys: Make sure 'delivery_id' and 'nas_id' are set correctly."):
        self.message = message
        super().__init__(self.message)


class MissingNetworkPropertiesError(Exception):
    """Exception indicating that EclipseCopy has invalid or unset port and ipv4 address."""

    def __init__(self, message="Invalid network configuration: Make sure 'ipv4__addr' and 'port' are set correctly."):
        self.message = message
        super().__init__(self.message)


class WellKnownPortError(Exception):
    """Exception indicating that user has attempted to use a well-known port."""
    def __init__(self, message="Port is in well-known range [0-1023]"):
        self.message = message
        super().__init__(self.message)
