"""ScriptRunner custom exceptions."""


class ScriptRunnerExc(BaseException):
    """Base ScriptRunner exception."""


class StopScriptRunnerExc(ScriptRunnerExc):
    """ScriptRunner `"stop"` keyword exception."""
