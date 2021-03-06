"""
Changing the default command parser

The cmdparser is responsible for parsing the raw text inserted by the
user, identifying which command/commands match and return one or more
matching command objects. It is called by Evennia's cmdhandler and
must accept input and return results on the same form. The default
handler is very generic so you usually don't need to overload this
unless you have very exotic parsing needs; advanced parsing is best
done at the Command.parse level.

The parser makes use of the cmdset to find command candidates. The
parser return a list of matches. Each match is a tuple with its first
three elements being the parsed cmdname (lower case), the remaining
arguments, and the matched cmdobject from the cmdset.

This module is not accessed by default. To tell Evennia to use it
instead of the default command parser, add the following line to
your settings file:

    COMMAND_PARSER = "server.conf.cmdparser.cmdparser"

"""

import json
from evennia.utils import logger
import evennia.commands.cmdparser as evennia_cmdparser


CMD_LOGINSTART = "__unloggedin_look_command"


def cmdparser(raw_string, cmdset, caller, match_index=None):
    """
    This function is called by the cmdhandler once it has
    gathered and merged all valid cmdsets valid for this particular parsing.

    raw_string - the unparsed text entered by the caller.
    cmdset - the merged, currently valid cmdset
    caller - the caller triggering this parsing
    match_index - an optional integer index to pick a given match in a
                  list of same-named command matches.

    Returns:
     list of tuples: [(cmdname, args, cmdobj, cmdlen, mratio), ...]
            where cmdname is the matching command name and args is
            everything not included in the cmdname. Cmdobj is the actual
            command instance taken from the cmdset, cmdlen is the length
            of the command name and the mratio is some quality value to
            (possibly) separate multiple matches.

    """
    # Parse JSON formated command.
    logger.log_infomsg("Receive command, %s: %s" % (caller, raw_string))

    try:
        data = json.loads(raw_string)
    except Exception:
        # Command is not in JSON, call evennia's cmdparser.
        return evennia_cmdparser.cmdparser(raw_string, cmdset, caller, match_index)

    cmd = data["cmd"]
    args = data["args"]

    # Find the matching command in cmdset.
    for cmdobj in cmdset:
        if cmdobj.key == cmd:
            return [(cmd, args, cmdobj, len(cmd), 1, raw_string)]

    # can not find
    return []

