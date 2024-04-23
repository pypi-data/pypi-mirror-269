# MIT License

# Copyright (c) 2024 Soumyo Deep Gupta

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
wrapper module for wrapping commands across a progressbar.
"""

from io import TextIOWrapper
from os import getcwd as pwd
from os.path import join as jPath, abspath
from time import sleep
from datetime import datetime
import progressbar
import subprocess

class Wrapper:
    """Wrapper Class: Wrap commands/scripts across a progress bar.
    
    `Usage:`
    >>> from wrapper_bar.wrapper import Wrapper
    
    >>> wrapControl = Wrapper(label="Loading:")
    >>> wrapControl.decoy() # for demonstration.
    
    `Other Functions include:`
    >>> wrapControl.shellWrapper(<params>) # wrap shell commands into a progress bar.
    >>> wrapControl.pyWrapper(<params>) # wrap python scripts into a progress bar.
    
    `Parameters:`
    # Wrapper class
    >>> wrapControl = Wrapper(label:str (optional), marker:str (optional))
    # decoy function
    >>> wrapControl.decoy(delay:float (optional), width:float (optional))
    # shellWrapper function
    >>> wrapControl.shellWrapper(shellcommands:list[str], delay:float (optional),
                                 width:float (optional), logger:bool (optional),
                                 logfile:TextIOWrapper (optional),
                                 logfile_auto_close:bool (optional))
    # pyWrapper function
    >>> wrapControl.pyWrapper(pythonscripts:list[str], delay:float (optional),
                                 width:float (optional), logger:bool (optional),
                                 logfile:TextIOWrapper (optional),
                                 logfile_auto_close:bool (optional))
    
    For Beginners, wrapping commands across a given progress bar might seem
    awfully time consuming. This Module is an effort to provide satisfaction to
    your aesthetic needs for your scripts.
    
    Feel free to check out the code and do any modifications you like under the
    MIT License. ;)
    """
    def __init__(self, label:str="", marker:str = "▓") -> None:
        """Initialize the Wrapper class"""
        self.label = label
        self.marker = marker
    
    def decoy(self, delay: float = 0.1, width:float = 50):
        """Create a decoy progress bar, that does nothing at all."""
        widgets = [self.label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
        
        for i in range(100):
            sleep(delay)
            bar.update(i)
        
        bar.finish()
    
    def shellWrapper(self, shellcommands: list[str], delay: float = 0.1, width:float = 50, logger:bool = False,
                     logfile:TextIOWrapper = None, logfile_auto_close:bool = False):
        """Wrap shell commands with the progressbar."""
        if logger:
            if not logfile:
                logfile = open(jPath(pwd(), '.log'), 'w')
        
        widgets = [self.label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        bar = progressbar.ProgressBar(widgets=widgets, term_width=width, maxval=100).start()
        
        interval = int(100/(len(shellcommands)+1))
        iterator = 0
        
        for i in range(100):
            if i>=interval and (i==interval or i%interval==0) and iterator<len(shellcommands):
                logfile.write(f"{datetime.today().strftime('%B %d, %Y')} {datetime.now().strftime('%H hours %M minutes %S seconds')}\n")
                logfile.write(f"Command Executed: \'{shellcommands[iterator]}\'\n")
                subprocess.Popen(shellcommands[iterator].split(' '), stderr=logfile, stdout=logfile).wait()
                logfile.write(f'\nEND\n')
                iterator += 1
                bar.update(i)
            else:
                sleep(delay)
                bar.update(i)
        
        bar.finish()
        
        if logfile_auto_close:
            logfile.close()
    
    def pyWrapper(self, pythonscripts: list[str], delay: float = 0.1, width: float = 50, logger:bool = False,
                  logfile: TextIOWrapper = None, logfile_auto_close:bool = False):
        """Wrap Python Scripts with the progressbar."""
        if logger:
            if not logfile:
                logfile = open(jPath(pwd(), '.log'), 'w')
        
        for i in range(len(pythonscripts)):
            pythonscripts[i] = abspath(pythonscripts[i])
        
        widgets = [self.label+" ", progressbar.Bar(marker=self.marker), progressbar.AdaptiveETA()]
        bar = progressbar.ProgressBar(widgets=widgets, maxval=100, term_width=width).start()
        
        interval = int(100/(len(pythonscripts)+1))
        iterator = 0
        
        for i in range(100):
            if i>=interval and (i==interval or i%interval==0) and iterator<len(pythonscripts):
                logfile.write(f"{datetime.today().strftime('%B %d, %Y')} {datetime.now().strftime('%H hours %M minutes %S seconds')}\n")
                logfile.write(f"Python File Executed: \'{pythonscripts[iterator]}\'\n")
                subprocess.Popen(['python'].extend(pythonscripts[iterator].split(' ')), stderr=logfile).wait()
                logfile.write(f"\nEND\n")
                iterator += 1
                bar.update(i)
            else:
                sleep(delay)
                bar.update(i)
        
        bar.finish()
        
        if logfile_auto_close:
            logfile.close()