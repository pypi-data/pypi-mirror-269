# MeerkatIO Python Package

## Introduction

[MeerkatIO](https://www.meerkatio.com/) is the personal notification platform for software developers and data scientists. Stop watching your code run and reclaim time in your day! Use this package to trigger personal notifications when your long running build or test processes finish, or to log output for personal debugging to an external communication channel.

Get started with just 2 lines of code!

## Installation

```bash
$ pip3 install meerkatio
```

## Authenticating

After creating an account at [MeerkatIO](http://meerkatio.com/register) you will be given a unique token which can be used to authenticate with the SDK. Your Meerkat token can either be set in your environment with the `MEERKAT_TOKEN` environmental variable or in the `~/.meerkat` file in your user’s home directory. No authentication is required to use the free Ping feature of MeerkatIO.

### Log In from the command line

```bash
$ meerkat login
```

### Or manually set the MeerkatIO token

```bash
# Environmental Variable
$ export MEERKAT_TOKEN=token

# Cache File
$ echo "token" > ~/.meerkat
```

## Code Examples

```python
import meerkat

# Ping when script gets to checkpoint
meerkat.ping()

# Send a confirmation a function has run
output = build_model()
meerkat.email(output)

# Send Slack message to document model performance
perf = get_model_performance(output)
meerkat.slack(perf)

# Send SMS message when the script is finished
meerkat.sms("Script completed!")
```

### Jupyter Notebook Example

```python
import meerkat

# Ping when cell hits a debug checkpoint
%ping

# Send a confirmation that a cell has run
output = build_model()
%email output

# Send Slack message to document model performance
perf = get_model_performance(output)
%slack perf

# Send SMS message when the cell reaches the end
%sms "Cell completed!"
```

![MeerkatIO Jupyter Notebook personal notification example alerting options](docs/jupyter_example.png)

## MeerkatIO CLI Tool
Access all of the same communication methods from your command prompt to integrate with any workflow.

```bash
$ meerkat ping
$ meerkat email "Bash script output: $1"
$ meerkat sms "Firmware build completed."
$ meerkat slack "Bash script complete"
```

Here is an example of how to use Meerkat with any script running from a terminal in order to ping youself when the script is finished running.

```bash
$ make build && meerkat email "Build succeeded" || meerkat sms "Build failed"
```