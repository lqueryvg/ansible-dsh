# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
from ansible import constants as C


class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'dsh'

    def _command_generic_msg(self, result, prefix):
        ''' output the result of a command run '''

        buf = prefix
        buf += result._result.get('stdout','').replace('\n', '\n' + prefix)
        buf += result._result.get('stderr','').replace('\n', '\n' + prefix)
        buf += result._result.get('msg','')
        return buf

    def _module_output(self, prefix, result, colour):
        buf = prefix
        if 'stdout_lines' in result._result:
            buf += ("\n" + prefix).join(result._result['stdout_lines'])
        else:
            buf += self._dump_results(result._result, indent=4).replace('\n', '\n' + prefix)

        self._display.display(buf, color=colour)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        colour = C.COLOR_ERROR
        if 'exception' in result._result:
            # TODO: how to test ?
            if self._display.verbosity < 3:
                # extract just the actual error message from the exception text
                error = result._result['exception'].strip().split('\n')[-1]
                msg = "An exception occurred during task execution. To see the full traceback, use -vvv. The error was: %s" % error
            else:
                msg = "An exception occurred during task execution. The full traceback is:\n" + result._result['exception']

            self._display.display(msg, color=colour)

        prefix = result._host.get_name() + ': ERROR: '
        if result._task.action in C.MODULE_NO_JSON:
            self._display.display(self._command_generic_msg(result, prefix), color=colour)
        else:
            prefix += 'rc=%s: ' % result._result.get('rc',0)
            self._module_output(prefix, result, colour)

    def v2_runner_on_ok(self, result):
        self._clean_results(result._result, result._task.action)

        prefix = result._host.get_name() + ': '
        colour = C.COLOR_OK

        if result._task.action in C.MODULE_NO_JSON:
            self._display.display(self._command_generic_msg(result, prefix), color=colour)
        else:
            if 'changed' in result._result and result._result['changed']:
                colour = C.COLOR_CHANGED # TODO how to test ?

            self._module_output(prefix, result, colour)
            self._handle_warnings(result._result)

    def v2_runner_on_skipped(self, result):
        # TODO test
        self._display.display("%s: SKIPPED" % (result._host.get_name()), color=C.COLOR_SKIP)

    def v2_runner_on_unreachable(self, result):
        self._display.display("%s: UNREACHABLE: %s" % (result._host.get_name(), result._result['msg']), color=C.COLOR_UNREACHABLE)
