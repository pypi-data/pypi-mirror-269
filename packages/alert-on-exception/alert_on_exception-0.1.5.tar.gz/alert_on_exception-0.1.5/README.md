# AlertOnException

`AlertOnException` is a Python library designed to send email notifications when exceptions occur in your applications. It is particularly useful for monitoring applications in production, ensuring you are immediately alerted to any issues that arise.

## Features

- Simple setup for sending email notifications.
- Customizable subject and message content.



## Installation

Install using below pip command

```bash
pip install alert-on-exception
```


To use ExceptionNotifier, you need to configure it with your SMTP details and the recipient's information. Here's a quick example:


```bash
from alert_on_exception import alert

# Create an instance of ExceptionNotifier
notifier = alert.AlertOnException("receiver@example.com", "Application Error", "An error has occurred!")

```
