
# Multikill 

# pip install killallappsinfolder

Tested against Windows 10 / Python 3.11 / Anaconda

# ProcKiller

`ProcKiller` is a Python utility designed to identify and terminate processes running on a Windows machine based on specific executable files found within given directories. It utilizes the Windows API through the `ctypes` library to manage processes.

## Features

- **Executable Filtering:** Search for executable files within specified directories.
- **Process Mapping:** Map running processes to executables.
- **Process Termination:** Terminate processes based on matching executable files.
- **Customizable Termination Criteria:** Include options for sending different signals and handling child processes.

## Usage

To use `ProcKiller`, run the script from the command line with directories as arguments, followed by the interval (in seconds) for repeated execution. Here’s how to invoke it:

```bash
python prockiller.py "C:\path\to\first\directory" "C:\path\to\second\directory" 60
```

This will search for executables in the specified directories and terminate any matching running processes every 60 seconds.

## Components

### Main Functions

- **get_command_line(pid):** Retrieves the command line used to start a process.
- **get_all_executables(folder, exeendings, filter_function):** Searches for executable files in a specified folder.
- **get_procs_to_kill(allexefiles_onlyexe, allfullpath):** Identifies running processes that should be terminated.
- **kill_running_procs(allprocsdic, ...):** Terminates the processes identified for termination.

### Class Definition

- **ProcKiller:** A class to encapsulate the functionality of finding and killing processes.

### Command-Line Interface

- The script can be executed directly from the command line with specified parameters for directories and execution interval.

## Code Example

```python
pki = (
ProcKiller(
    folders=(
        r"C:\ProgramData\BlueStacks_nxt",
        r"C:\Program Files\Oracle",
        r"C:\Program Files\BlueStacks",
        r"C:\Program Files\BlueStacks_nxt",
    ),
    kill_timeout=2,
    protect_myself=True,  # important, protect_myselfis False, you might kill the whole python process you are in.
    winkill_sigint_dll=True,  # dll first
    winkill_sigbreak_dll=True,
    winkill_sigint=True,  # exe from outside
    winkill_sigbreak=True,
    powershell_sigint=True,
    powershell_sigbreak=True,
    powershell_close=True,
    multi_children_kill=False,  # try to kill each child one by one
    multi_children_always_ignore_pids=(0, 4),  # ignore system processes
    print_output=True,
    taskkill_as_last_option=True,  # this always works, but it is not gracefully anymore):
    exeendings=(".com", ".exe"),
    filter_function=lambda files: True,
)
.get_active_procs()
.kill_running_procs()
)
# Use it again to keep on killing
pki()
```

## Contributions

Contributions are welcome! If you find a bug or have suggestions for improvements, please open an issue or submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
