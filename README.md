## Time Tracker
A simple Python application to monitor the working time. The application displays the working time of the day and
compute the extra hours according to the number of hours per day. The working time per week is also computed and
stored but the application does not use it. This information is available in the `timetracker.json` file.

### Installation and Configuration
* Clone the repository
```
git clone https://github.com/info7tik/time-tracker.git
```
* Note the absolute path to the time-tracker directory
```
cd time-tracker
pwd
> /home/user/time-tracker
```
* Configure the path to the time-tracker configuration file by editing [timetracker.py](timetracker.py):
```
JSON_FILE = "/home/user/time-tracker/timetracker.json"
```
* (optional) Configure the number of working hours per day (default value is 7 hours/day)
  by editing [timetracker.py](timetracker.py):
```
NB_WORKING_HOURS_PER_DAY = 7
```
* Install the dependency
```
sudo apt install python3-tk
```

* Install the program in your path
```
sudo ln -s /home/user/time-tracker/trackergui.py /usr/bin/timetracker
```
**NOTE**: Do not move the `time-tracker` directory after this operation!

### How to use it
* Run the `timetracker` program, we should see the graphical interface
![alt TimeTracker GUI](./images/timetracker.png "Simple TimeTracker GUI)
* `Start` the counter while you start to work
* `Stop` the counter during your breaks
* `Delete` all the data to reset the counter (data will be lost)
