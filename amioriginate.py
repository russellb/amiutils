#!/usr/bin/env python

#
# Copyright (C) 2012, Russell Bryant
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

'''Originate a call on an Asterisk server

Developed as an example for "Asterisk: The Definitive Guide"
'''

import getpass
import logging
import optparse
import sys

import starpy.manager
from twisted.internet import reactor


LOG = logging.getLogger(__name__)


class OriginateCall(object):
    def __init__(self, options, channel):
        self.options = options
        self.channel = channel
        self.ami = starpy.manager.AMIFactory(self.options.username,
                                             self.options.password)

    def _on_login(self, ami):
        kwargs = dict(channel=self.channel, async=True)

        if self.options.application:
            kwargs['application'] = self.options.application
            kwargs['data'] = self.options.data
        else:
            kwargs['context'] = self.options.context
            kwargs['exten'] = self.options.exten
            kwargs['priority'] = self.options.priority

        def _on_success(ami):
            reactor.stop()

        def _on_error(reason):
            LOG.error('Originate failed: %s' % reason.getErrorMessage())
            reactor.stop()

        ami.originate(**kwargs).addCallbacks(_on_success, _on_error)

    def connect_and_call(self):
        def _on_login_error(reason):
            LOG.error('Failed to log in: %s' % reason.getErrorMessage())
            reactor.stop()

        df = self.ami.login(self.options.host, self.options.port)
        df.addCallbacks(self._on_login, _on_login_error)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    logging.basicConfig(level=logging.INFO)

    description = ('This program is used to originate a call on an Asterisk '
                   'server using the Asterisk Manager Interface (AMI). The '
                   'channel argument to this application tells Asterisk what '
                   'outbound call to make. There are various options that '
                   'can be used to specify what the outbound call is '
                   'connected to once it answers.')
    usage = '%prog [options] <channel>'

    parser = optparse.OptionParser(description=description, usage=usage)

    parser.add_option('-d', '--debug', action='store_true',
                      dest='debug', help='Enable debug output')
    parser.add_option('-u', '--username', action='store', type='string',
                      dest='username', default=None, help='AMI username')
    parser.add_option('-p', '--password', action='store', type='string',
                      dest='password', default=None, help='AMI password')
    parser.add_option('-H', '--host', action='store', type='string',
                      dest='host', default='localhost',
                      help='Hostname or IP address of the Asterisk server')
    parser.add_option('-t', '--port', action='store', type='int',
                      dest='port', default=5038,
                      help='Port number for the AMI')

    parser.add_option('-a', '--application', action='store', type='string',
                      dest='application', default='',
                      help='Application to connect the call to. When using '
                           'this option, you may also specify arguments to '
                           'the application with the -D/--data option. Do '
                           'not use this option and the context, extension, '
                           'and priority options at the same time.')
    parser.add_option('-D', '--data', action='store', type='string',
                      dest='data', default='',
                      help='Arguments to pass to the dialplan application '
                           'specified with -a/--application.')

    parser.add_option('-c', '--context', action='store', type='string',
                      dest='context', default='',
                      help='Context in the dialplan to send the call to '
                           'once it answers. If using this option, you '
                           'must also specify an extension and priority. '
                           'Do not specify the application or data options '
                           'if using this option.')
    parser.add_option('-e', '--extension', action='store', type='string',
                      dest='exten', default='',
                      help='Extension to connect the call to. This should '
                           'be used along with the context and priority '
                           'options.')
    parser.add_option('-P', '--priority', action='store', type='string',
                      dest='priority', default='',
                      help='Priority of the extension to connect the call '
                           'to. This should used along with the context '
                           'and extension options.')

    (options, args) = parser.parse_args(argv)

    if options.debug:
        LOG.setLevel(logging.DEBUG)
        starpy.manager.log.setLevel(logging.DEBUG)

    if len(args) != 2 or not len(args[1]):
        LOG.error('Please specify a single outbound channel.')
        parser.print_usage()
        return 1
    channel = args[1]

    valid_application = len(options.application)
    valid_extension = (len(options.context) and len(options.exten) and
                       len(options.priority))

    if not valid_application and not valid_extension:
        LOG.error('Please specify a valid point to connect the call to once '
                  'it answers.  Either specify an application or a context, '
                  'extension, and priority.')
        parser.print_usage()
        return 1

    if valid_application and valid_extension:
        LOG.error('Please specify only one of extension and application.')
        parser.print_usage()
        return 1

    if not options.username:
        user = raw_input('Username [%s]: ' % getpass.getuser())
        if not user:
            user = getpass.getuser()
        options.username = user

    if not options.password:
        options.password = getpass.getpass()

    o = OriginateCall(options, channel)
    reactor.callWhenRunning(o.connect_and_call)
    reactor.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
