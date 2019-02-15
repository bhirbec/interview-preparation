# Operating System

## What Is an OS?

- Load and manage processes 
- provide interfaces to hardwares via system calls 
- provide filesystem 
- provide a basic user interface

Example of OS:

- windows
- Unix:
	- Linux 
	- BSD
	- OS X

### Driver
OS plug-in module for controlling a particular device. Handle IO for a device (mouse, video card...) 

### Scheduler

Scheduling is the method by which thread, processes or data flows are given access to system resouces. OS allows multiple processes to run simoustanously. Each CPU alternates between running processes. That the scheduler responsibility to decide which processes to run. It may use round-robin or more elaborate strategies.

#### Round-robin

Time slices (Time Quatum) are assigned to each process in equal portion and in circular order, handling all processes without priority.

Maintaining scheduling queue of processes:
- job queue: set of all processes in the system 
- ready queue: set of all processes redising in main memeory (ready and waiting to execute) 
- device queue: set of processes waiting for I/O

Two kind of schedulers:
- long term: select which processes should be brougth in memory and invoked less frequently - may be slow
- short term: select which processes should be executed next and allocates CPU. Invoked very frequently (millisecond) - must be fast

### Memory

Processes not only share CPU but also memory. It's the OS job to regulate the processes use of memory and make sure each process can only access its own memory. 

CPU can run with 2 privilege levels:
- when OS code run CPU privilege allow access to entire device memory
- when processes run CPU privilege is restrincted to a specific portion of the memory and a hardware exception is thrown when the process tries to access other portion of the memory

Process memory:
- text (code itself)
- call stack: local variable, stack function calls
- heap: other data to store

### Stack

### System Calls
Process can invoke the OS via system calls. 

### Processes

Several states:
- created
- waiting: waiting to be selected by the scheduler
- running
- blocked: the process cannot run (usually due to sys call like reading a file)
- terminated

Processes can be described as either:
- I/O-bound
- CPU-bound

### HD

Divided in partion
Filesystem is a abstraction above storage devices and make possible to organize the data 

### IPC (Interprocess communication)

Umbrella to put any mechanism of the OS that facilitate communication between processes:
- files
- pipes
- sockets
- signals
- shared memory

