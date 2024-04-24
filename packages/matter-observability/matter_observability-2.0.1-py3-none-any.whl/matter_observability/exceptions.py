from matter_exceptions import DetailedException


class MisConfigurationError(DetailedException):
    TOPIC = "Configuration Error"
