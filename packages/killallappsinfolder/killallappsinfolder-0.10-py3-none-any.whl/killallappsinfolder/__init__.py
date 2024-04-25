from consolectrlchandler import ctrl_config
import sys
import os
import ctypes
from ctypes import wintypes
import itertools
import time
from list_all_files_recursively_short import get_folder_file_complete_path
from procciao import kill_proc
from ctypesprocstuff import iter_process, get_kids_dict
from flatten_any_dict_iterable_or_whatsoever import fla_tu

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

windll = ctypes.LibraryLoader(ctypes.WinDLL)
kernel32 = windll.kernel32
psapi = ctypes.WinDLL("Psapi.dll")

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

GetModuleFileNameExW = psapi.GetModuleFileNameExW
GetModuleFileNameExW.argtypes = [
    wintypes.HANDLE,
    wintypes.HMODULE,
    wintypes.LPWSTR,
    wintypes.DWORD,
]
GetModuleFileNameExW.restype = wintypes.DWORD


def ctrlhandler(ctrl_type: str):
    """
    A handler function for control actions, prints the control type received.

    Args:
        ctrl_type (str): The type of control action being handled.
    """
    print(f"ctrl handler {ctrl_type}")


ctrl_config.function = ctrlhandler


def get_command_line(pid: int) -> str:
    """
    Retrieves the command line path for a given process identifier.

    Args:
        pid (int): The process ID for which the command line path is required.

    Returns:
        str: The command line path of the process if successful, an empty string otherwise.
    """
    hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    bu2 = ""
    try:
        buffer2 = ctypes.create_unicode_buffer(1024)
        if GetModuleFileNameExW(hProcess, None, buffer2, 1024):
            bu2 = str(buffer2.value)
    except Exception as e:
        print(e)
    finally:
        try:
            kernel32.CloseHandle(hProcess)
        except Exception as e:
            print(e)
    return bu2


def get_all_executables(
    folder: str,
    exeendings: tuple[str] = (".com", ".exe"),
    filter_function=lambda files: True,
) -> tuple[list[str], list, list[str]]:
    """
    Retrieves all executable files from a specified folder that match given extensions.

    Args:
        folder (str): The folder path to search in.
        exeendings (tuple[str]): A tuple containing the file extensions to filter by.
        filter_function (callable): A function used to further filter the files.

    Returns:
        tuple: A tuple containing lists of filenames, files with details, and full paths of executables.
    """
    allfiles = get_folder_file_complete_path(folder, use_cache=False)
    allfiles = [x for x in allfiles if filter_function(x)]
    allexefiles = [x for x in allfiles if x.ext.lower() in exeendings]
    allexefiles_onlyexe = [x.file.lower() for x in allexefiles] + [
        x.name83.rsplit(os.sep)[-1].lower() for x in allexefiles
    ]
    allfullpath = [x.path.lower() for x in allexefiles] + [
        x.name83.lower() for x in allexefiles
    ]
    return allexefiles_onlyexe, allexefiles, allfullpath


def get_procs_to_kill(allexefiles_onlyexe: list[str], allfullpath: list[str]) -> dict:
    """
    Filters processes that need to be terminated based on executable names and paths.

    Args:
        allexefiles_onlyexe (list[str]): List of executable names to check against running processes.
        allfullpath (list[str]): List of full paths of executables to check against running processes.

    Returns:
        dict: A dictionary containing process IDs and details of processes that need to be killed.
    """
    procs = list(iter_process())
    procsfiltered = [x for x in procs if x.szExeFile.lower() in allexefiles_onlyexe]
    allprocsdic = {}
    for p in procsfiltered:
        c1 = get_command_line(p.th32ProcessID)
        if c1.lower() in allfullpath:
            qq = get_kids_dict(pid=p.th32ProcessID, bi_rl_lr="lr")
            allprocsdic[p.th32ProcessID] = qq
    return allprocsdic


def kill_running_procs(
    allprocsdic: dict,
    kill_timeout: int = 2,
    protect_myself: bool = True,
    winkill_sigint_dll: bool = True,
    winkill_sigbreak_dll: bool = True,
    winkill_sigint: bool = True,
    winkill_sigbreak: bool = True,
    powershell_sigint: bool = True,
    powershell_sigbreak: bool = True,
    powershell_close: bool = True,
    multi_children_kill: bool = False,
    multi_children_always_ignore_pids: tuple = (0, 4),
    print_output: bool = True,
    taskkill_as_last_option: bool = True,
):
    """
    Terminates running processes based on provided dictionary of process details.

    Args:
        allprocsdic (dict): Dictionary containing process IDs and details for termination.
        kill_timeout (int): Timeout in seconds before force termination.
        protect_myself (bool): Flag to prevent termination of the calling process.
        winkill_sigint_dll (bool): Use DLL for sending SIGINT.
        winkill_sigbreak_dll (bool): Use DLL for sending SIGBREAK.
        winkill_sigint (bool): Send SIGINT to terminate processes.
        winkill_sigbreak (bool): Send SIGBREAK to terminate processes.
        powershell_sigint (bool): Use PowerShell for sending SIGINT.
        powershell_sigbreak (bool): Use PowerShell for sending SIGBREAK.
        powershell_close (bool): Use PowerShell to close processes.
        multi_children_kill (bool): Option to try to kill child processes individually.
        multi_children_always_ignore_pids (tuple): PIDs to always ignore when killing.
        print_output (bool): Flag to enable printing output of the termination process.
        taskkill_as_last_option (bool): Use taskkill as the last option for termination.
    """
    killprocids = {}
    for k, v in allprocsdic.items():
        pids = list(fla_tu(v))
        if k not in killprocids:
            killprocids[k] = []
        for k2, v2 in pids:
            for psub in itertools.takewhile(lambda q: isinstance(q, int), v2):
                if psub not in killprocids[k]:
                    killprocids[k].append(psub)

    for k, v in killprocids.items():
        for v2 in reversed(v):
            kill_proc(
                v2,
                kill_timeout=kill_timeout,
                protect_myself=protect_myself,
                winkill_sigint_dll=winkill_sigint_dll,
                winkill_sigbreak_dll=winkill_sigbreak_dll,
                winkill_sigint=winkill_sigint,
                winkill_sigbreak=winkill_sigbreak,
                powershell_sigint=powershell_sigint,
                powershell_sigbreak=powershell_sigbreak,
                powershell_close=powershell_close,
                multi_children_kill=multi_children_kill,
                multi_children_always_ignore_pids=multi_children_always_ignore_pids,
                print_output=print_output,
                taskkill_as_last_option=taskkill_as_last_option,
            )


class ProcKiller:
    def __init__(
        self,
        folders,
        kill_timeout: int = 2,
        protect_myself: bool = True,
        winkill_sigint_dll: bool = True,
        winkill_sigbreak_dll: bool = True,
        winkill_sigint: bool = True,
        winkill_sigbreak: bool = True,
        powershell_sigint: bool = True,
        powershell_sigbreak: bool = True,
        powershell_close: bool = True,
        multi_children_kill: bool = False,
        multi_children_always_ignore_pids: tuple = (0, 4),
        print_output: bool = True,
        taskkill_as_last_option: bool = True,
        exeendings: tuple[str] = (".com", ".exe"),
        filter_function=lambda files: True,
    ):
        r"""
            Initializes the ProcKiller class with the necessary attributes to find and kill processes.

                Args:
                    folders (list[str]): Directories to search for executable files.
                    kill_timeout (int): Timeout in seconds before force termination.
                    protect_myself (bool): Prevent termination of the calling process.
                    winkill_sigint_dll (bool): Use DLL for sending SIGINT.
                    winkill_sigbreak_dll (bool): Use DLL for sending SIGBREAK.
                    winkill_sigint (bool): Send SIGINT to terminate processes.
                    winkill_sigbreak (bool): Send SIGBREAK to terminate processes.
                    powershell_sigint (bool): Use PowerShell for sending SIGINT.
                    powershell_sigbreak (bool): Use PowerShell for sending SIGBREAK.
                    powershell_close (bool): Use PowerShell to close processes.
                    multi_children_kill (bool): Option to try to kill child processes individually.
                    multi_children_always_ignore_pids (tuple): PIDs to always ignore when killing.
                    print_output (bool): Enable printing output of the termination process.
                    taskkill_as_last_option (bool): Use taskkill as the last option for termination.
                    exeendings (tuple[str]): Executable file extensions to look for.
                    filter_function (callable): Function to filter files.
            Example:
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
        # CLI - as many folders as you want + time to sleep in seconds after killing
        # python killallappsinfolder.py c:\folder1 c:\folder2 15
        """
        self.exeendings = exeendings
        self.filter_function = filter_function
        self.folders = folders
        self.kill_timeout = kill_timeout
        self.protect_myself = protect_myself
        self.winkill_sigint_dll = winkill_sigint_dll
        self.winkill_sigbreak_dll = winkill_sigbreak_dll
        self.winkill_sigint = winkill_sigint
        self.winkill_sigbreak = winkill_sigbreak
        self.powershell_sigint = powershell_sigint
        self.powershell_sigbreak = powershell_sigbreak
        self.powershell_close = powershell_close
        self.multi_children_kill = multi_children_kill
        self.multi_children_always_ignore_pids = multi_children_always_ignore_pids
        self.print_output = print_output
        self.taskkill_as_last_option = taskkill_as_last_option
        self.files_onlyexe, self.files_all, self.files_onlyfullpath = (
            get_all_executables(
                self.folders,
                exeendings=self.exeendings,
                filter_function=self.filter_function,
            )
        )
        self.found_procs = {}

    def __repr__(self) -> str:
        return "\n".join(str(k) for k in self.files_all)

    def __str__(self) -> str:
        return self.__repr__()

    def __call__(self):
        return self.get_active_procs().kill_running_procs()

    def get_active_procs(self) -> "ProcKiller":
        """
        Identifies and lists all active processes that need to be terminated based on the executables found.

        Returns:
            self: Returns an instance of itself with the active processes loaded.
        """
        self.found_procs = get_procs_to_kill(
            self.files_onlyexe, self.files_onlyfullpath
        )
        return self

    def kill_running_procs(self) -> "ProcKiller":
        """
        Executes the process termination for all active processes listed in `found_procs`.

        Returns:
            self: Returns an instance of itself after attempting to kill the processes.
        """
        kill_running_procs(
            self.found_procs,
            kill_timeout=self.kill_timeout,
            protect_myself=self.protect_myself,
            winkill_sigint_dll=self.winkill_sigint_dll,
            winkill_sigbreak_dll=self.winkill_sigbreak_dll,
            winkill_sigint=self.winkill_sigint,
            winkill_sigbreak=self.winkill_sigbreak,
            powershell_sigint=self.powershell_sigint,
            powershell_sigbreak=self.powershell_sigbreak,
            powershell_close=self.powershell_close,
            multi_children_kill=self.multi_children_kill,
            multi_children_always_ignore_pids=self.multi_children_always_ignore_pids,
            print_output=self.print_output,
            taskkill_as_last_option=self.taskkill_as_last_option,
        )
        return self


if __name__ == "__main__":
    if len(sys.argv) > 1:
        time2repeat = int(sys.argv[-1].strip())
        allfolderstmp = sys.argv[1:-1]
        allfolders = []
        for k in allfolderstmp:
            k2 = k.strip(" \"'")
            if os.path.exists(k2):
                allfolders.append(k2)
            elif os.path.exists(k):
                allfolders.append(k)
            else:
                sys.stderr.write("Folder not found: " + k2 + "\n")
                sys.stderr.flush()

        pki = ProcKiller(
            folders=allfolders,
            kill_timeout=2,
            protect_myself=True,
            winkill_sigint_dll=True,
            winkill_sigbreak_dll=True,
            winkill_sigint=True,
            winkill_sigbreak=True,
            powershell_sigint=True,
            powershell_sigbreak=True,
            powershell_close=True,
            multi_children_kill=False,
            multi_children_always_ignore_pids=(0, 4),
            print_output=True,
            taskkill_as_last_option=True,
            exeendings=(".com", ".exe"),
            filter_function=lambda files: True,
        )
        while True:
            pki.get_active_procs().kill_running_procs()
            time.sleep(time2repeat)
