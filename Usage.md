# Usage

## Select OS Environments

### Windows
> You just need to **pip install -r mock_gui/requirements.txt** and run the project in Python 3.12 environment
 
### Linux
> When running this project with Docker build and run. See the `Build` and `Run` items below


## Build

> The commands below **cannot be modified**. Be sure to implement the Dockerfile so that it can run.
> If you need more than one `Dockerfile` , you can add the command below.

```bash
docker build --tag cs-project .
```

## Run

> Please replace the `run-argument` and `argument` items with specific descriptions.

The following argument is required to use the hardware resources of a Linux host

If the host's hardware is not used, the host's hardware settings are incorrect.
```bash
docker run --rm cs-project --ipc=host --privileged --device /dev/snd --device /dev/video0 -v /etc/asound.conf:/etc/asound.conf -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/user/Desktop/workspace:/mnt/workspace -e DISPLAY=$DISPLAY -e Lang=C.UTF-8 -e QT_X11_NO_MITSHM=1
```

## Control

> Describe in detail below how to use a running container for its purpose.

### How to use it
1. Add a cover letter
2. Interview Starts
3. Check summary and evaluation after the interview is over

### How to create and use a customized interviewer
1. Conduct the interview after agreeing to collect the contents of the interview
2. Click on a customized interviewer button
3. Create and use customized interviewers