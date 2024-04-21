from __future__ import annotations
import signal
import subprocess as subp
import sys
import threading as th

import time
from typing import Any
import os


class CLITool:
    "Shell command."
    def __init__(self, name:str) -> None:
        "A class that represents a shell command."
        self.name = name
        self.process:subp.Popen = None
        self.pipe_in:bytes | CLITool = None
        self.args = []
        self.thread:th.Thread = None
        self._stderr:bytes = None
        self._stdout:bytes = None
        self.pipe_err = False
        self.concurrent = False
        self.has_run = False

    def __call__(self, *args: Any) -> CLITool:
        self.args = [self.name, *[str(arg) for arg in args]]
        return self
    
    def finish(self):
        "Blocks code untill process is finished.  Basically the same as `.join()`ing the thread."
        if self.thread != None:
            self.thread.join()
        else:
            raise RuntimeError("Concurrent process is not running.")

    
    def _run(self):
        "Run the command."
        self.process = subp.Popen(" ".join(self.args), shell=True,
            stdout=subp.PIPE, stderr=subp.PIPE, stdin=subp.PIPE)
        
        pipe_in = b''

        if isinstance(self.pipe_in, CLITool):
            if self.pipe_err:
                if not self.pipe_in.has_run:
                    self.pipe_in.run()
                pipe_in = self.pipe_in.stderr
            else:
                if not self.pipe_in.has_run:
                    self.pipe_in.run()
                pipe_in = self.pipe_in.stdout
        else:
            pipe_in = self.pipe_in

        #print(self.name, "RUNNING")
        self._stdout, self._stderr = self.process.communicate(pipe_in)

        return self
    
    def run(self):
        "Runs the process."
        self.has_run = True
        if self.concurrent:
            return self._run_concurrent()
        else:
            return self._run()
    
    def _run_concurrent(self):
        "Runs process on a separate thread."
        self.thread = th.Thread(target=lambda:self._run())
        self.thread.start()
        return self
    
    def __invert__(self):
        "`&`\n\nRuns process on a separate thread."
        self.concurrent = True
        return self

    def __or__(self, other:CLITool | Any):
        "`|`\n\nPipe stdout into right hand side as a string."
        if isinstance(other, CLITool):
            other.pipe_in = self
            return other
        else:
            raise TypeError("Cant stdout pipe Shell command into type other than another shell command")
    
    def __ror__(self, other:Any):
        "`|`\n\nPipe python type into right hand side as a string."
        self.pipe_in = str(other).encode()
        return self
    
    def __matmul__(self, other:CLITool):
        "`|&`\n\nPipe stderr into right hand side as a string.."
        if isinstance(other, CLITool):
            other.pipe_in = self
            other.pipe_err = True
            return other
        else:
            raise TypeError("Cant stderr pipe Shell command into type other than another shell command")
        
    def kill(self):
        "Kills the process."
        if self.running:
            os.kill(self.pid, signal.SIGTERM)
        else:
            raise RuntimeError(f"Tried to kill process that doesnt exist with pid:({self.pid}).")
        return self
        
    @property
    def running(self):
        "Returns True if the process is running, False if not."
        if self.thread != None:
            return self.thread.is_alive()
        return False
    
    @property
    def pid(self):
        if self.process != None:
            return self.process.pid
        return None
    
    @property
    def stdout(self):
        if self._stdout != None:
            return self._stdout
        elif self.thread != None:
            self.thread.join()
        return self._stdout
    
    @property
    def stderr(self):
        if self._stderr != None:
            return self._stderr
        elif self.thread != None:
            self.thread.join()
        return self._stderr

class Shell:
    def __getattribute__(self, name: str) -> CLITool:
        "Shell command."
        return CLITool(name)
    def __getitem__(self, name: str) -> CLITool:
        "Shell command."
        return CLITool(name)
    def __getattr__(self, name: str) -> CLITool:
        "Shell command."
        return CLITool(name)
    
SHELL = Shell()

if __name__ == "__main__":
    process, process_err = ~((p1 := (SHELL.echo("SHELL") | SHELL.tee("/dev/stderr"))) | SHELL.grep("SHELL")), ~(p1 @ SHELL.grep("SHELL"))
    p1.run()
    process.run()
    process_err.run()
    
    print(f"p_out:\n{process.stdout.decode()}")
    print(f"p_err:\n{process_err.stdout.decode()}")