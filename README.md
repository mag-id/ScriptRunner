# ScriptRunner

## Description
The final project for EPAM Autumn 2020 Python Course is **ScriptRunner - script launcher on a server with a web interface.**

## Original requirements

1. Application:
 * The app starts on a remote server.
 * The app has a configuration with a scripts folder and script configurations folder.
 * Scripts without configurations are not run.
2. Script configuration:
 * Run parameters.
 * Run priority.
 * What to do while scrips errors.
 * Which script to run next (must have configuration).
3. Functionality:
 * Script configuration edit form.

## ScriptRunner v.1 functionality (Python 3.8.7)

* **Only Python scripts!**
* See and update script configs.
* See scripts and their code.
* Submit scripts queue.
* Use `"skip"` and `"stop"` keywords for controlling exception processing.

### Script config format

```
{
    "priority": 0,
    "script": "name.py",
    "arguments": ["arg", "arg"],
    "failures": "stop",
    "next_config": false
}
```

* `"priority"` - Integer represents task priority.
* `"script"` - Name of the Python script.
* `"arguments"` - Script arguments.
* `"failures"` - Specific keywords for controlling exception processing:
    * `"skip"` - skip exception and go to the next task.
    * `"stop"` - stop scripts queue execution.
* `"next_config"` - deside what do after:
    * `"false"` - executes next script from queue according to their priopities.
    * `"name.json"` - script config which will be executed next out of priority.
