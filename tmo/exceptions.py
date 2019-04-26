class TMOException(Exception):
    """Base Exception class for tmo module exceptions."""
    pass


class FormatterNotSet(TMOException):
    """Exception raised when formatter is not set on tmo engine"""
    pass


class FormatterInvalid(TMOException):
    """Exception raised when formatter is not subclassing string.Formatter"""
    pass


class TemplatesNotInitialized(TMOException):
    """Exception raised when templates are not initalized on tmo engine"""
    pass
