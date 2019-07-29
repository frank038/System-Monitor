# System-Monitor
by frank038

v. 1.0

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY. Anyone can use and modified it for any purpose. Just remember the author (in case of modification).

A linux system monitor in Python3/tkinter for monitoring cpu (and gpu).

The first graph shows the cpu load: when the mouse is over it, the value at that point is shown in the label on the left and also the cpu frequencies at that point in the labels below.

The second graph shows the cpu temperature in the same manner.

The gpu part of the program shows the same infos as the cpu, but the program nvidia-smi is needed.

Each sensor can be enabled and disabled. A pause button is present.

An optional argument can be passed to the program, the interval in seconds, e.g.: ./system-monitor.py 3.

Some kind of personalization is possible by changing some values at the beginning of the script.

![My image](https://github.com/frank038/System-Monitor/blob/master/sm1.png)
