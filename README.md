# job_scheduler

This is a simple yet enough powerful job scheduler engine.

The entry point consists of runDMScheduler.pl - a perl file that is only responsible for sending the
log file of the entire process to the recepients (support team).

The main scheduling logic lies in runDatamix_Scheduler.py - a python script that uses Win32 & cross platform
process synchronization primitives to ensure that a constant number of concurrent jobs (processes) is run at
all times. That is it spawns (batchsize)number of concurrent jobs and waits for any of them to finish.
Upon job completion, the next available job is pushed to the queue until all jobs are iterated.

Datamix.py is an example of such a job. It splits it's calculation logic across 11 different servers and
waits for all the parts to complete. Upon completion, it merges the results onto a single file and pushes
them onto a remote FTP server.

Spawner.py is a utility - it is meant to guarantee successful run of every single "batch", by using a
check and retry mechanism. Therefore, even in high DB utilization scenarios, it will do it's best to
make sure the requested computation unit is successfully run and has produced results.
