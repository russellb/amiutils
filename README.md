AMI Utils
=========

Utilities that interact with the Asterisk Manager Interface (AMI).

 * amioriginate.py - originate a call

```
$ ./amioriginate.py --help
Usage: amioriginate.py [options] <channel>

This program is used to originate a call on an Asterisk server using the
Asterisk Manager Interface (AMI). The channel argument to this application
tells Asterisk what outbound call to make. There are various options that can
be used to specify what the outbound call is connected to once it answers.

Options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug output
  -u USERNAME, --username=USERNAME
                        AMI username
  -p PASSWORD, --password=PASSWORD
                        AMI password
  -H HOST, --host=HOST  Hostname or IP address of the Asterisk server
  -t PORT, --port=PORT  Port number for the AMI
  -a APPLICATION, --application=APPLICATION
                        Application to connect the call to. When using this
                        option, you may also specify arguments to the
                        application with the -D/--data option. Do not use this
                        option and the context, extension, and priority
                        options at the same time.
  -D DATA, --data=DATA  Arguments to pass to the dialplan application
                        specified with -a/--application.
  -c CONTEXT, --context=CONTEXT
                        Context in the dialplan to send the call to once it
                        answers. If using this option, you must also specify
                        an extension and priority. Do not specify the
                        application or data options if using this option.
  -e EXTEN, --extension=EXTEN
                        Extension to connect the call to. This should be used
                        along with the context and priority options.
  -P PRIORITY, --priority=PRIORITY
                        Priority of the extension to connect the call to. This
                        should used along with the context and extension
                        options.
```
