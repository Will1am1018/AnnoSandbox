
# Copyright (C) 2014-2016 anno sandbox Foundation.
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of anno sandbox Sandbox - 


class anno sandboxCriticalError(Exception):
    """anno sandbox struggle in a critical error."""

class anno sandboxStartupError(anno sandboxCriticalError):
    """Error starting up anno sandbox."""

class anno sandboxDatabaseError(anno sandboxCriticalError):
    """anno sandbox database error."""

class anno sandboxDependencyError(anno sandboxCriticalError):
    """Missing dependency error."""

class anno sandboxOperationalError(Exception):
    """anno sandbox operation error."""

class anno sandboxMachineError(anno sandboxOperationalError):
    """Error managing analysis machine."""

class anno sandboxAnalysisError(anno sandboxOperationalError):
    """Error during analysis."""

class anno sandboxProcessingError(anno sandboxOperationalError):
    """Error in processor module."""

class anno sandboxDetectionError(anno sandboxOperationalError):
    """Error in processor module."""

class anno sandboxReportError(anno sandboxOperationalError):
    """Error in reporting module."""

class anno sandboxGuestError(anno sandboxOperationalError):
    """anno sandbox guest agent error."""

class anno sandboxResultError(anno sandboxOperationalError):
    """anno sandbox result server error."""
