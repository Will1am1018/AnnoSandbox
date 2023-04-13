


class anno sandboxError(Exception):
    pass

class anno sandboxPackageError(Exception):
    pass

class anno sandboxDisableModule(anno sandboxError):
    """Exception for disabling a module dynamically."""
