"""ScriptRunner custom exceptions."""


class ScriptRunnerException(BaseException):
    """Base ScriptRunner exception."""


class FailuresException(ScriptRunnerException):
    """Failures parent exception."""


class StopKeywordFailures(FailuresException):
    """ScriptRunner `"stop"` keyword exception."""


class UnknownKeywordFailures(FailuresException):
    """ScriptRunner unknown keyword exception."""
