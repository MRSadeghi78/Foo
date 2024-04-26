import enum


class UserRole(enum.Enum):
    """
        Enumeration representing user roles.

        Defines two roles: ADMIN and CUSTOMER.
    """
    ADMIN = 'admin'
    CUSTOMER = 'customer'
