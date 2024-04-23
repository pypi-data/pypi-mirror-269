Assorted debugging facilities.

*Latest release 20240423*:
* Support "import *" by populating __all__ with X, r, s, TimingOutLock, thread_dump, stack_dump, trace.
* @trace: include the elapsed time on the return/exception log message.

If the environment variable $CS_DEBUG_BUILTINS is set to a comma
separated list of names then the `builtins` module will be monkey
patched with those names, enabling trite debug use of those names
anywhere in the code provided this module has been imported somewhere.
The allowed names are the list `cs.debug.__all__` and include:
* `X`: `cs.x.X`
* `breakpoint`: `cs.upd.breakpoint`
* `pformat`: `pprint.pformat`
* `pprint`: `pprint.pprint`
* `print`: `cs.upd.print`
* `r`: `cs.lex.r`
* `redirect_stdout`: `contextlib.redirect_stdout`
* `s`: `cs.lex.s`
* `stack_dump`: dump current `Thread`'s call stack
* `thread_dump` dump the active `Thread`s with their call stacks
* `trace`: the `@trace` decorator
`$CS_DEBUG_BUILTINS` can also be set to `"1"` to install all of
`__all__` in the builtins.

## Function `stack_dump(stack=None, limit=None, logger=None, log_level=None)`

Dump a stack trace to a logger.

Parameters:
* `stack`: a stack list as returned by `traceback.extract_stack`.
  If missing or `None`, use the result of `traceback.extract_stack()`.
* `limit`: a limit to the number of stack entries to dump.
  If missing or `None`, dump all entries.
* `logger`: a `logger.Logger` ducktype or the name of a logger.
  If missing or `None`, obtain a logger from `logging.getLogger()`.
* `log_level`: the logging level for the dump.
  If missing or `None`, use `cs.logutils.loginfo.level`.

## Function `thread_dump(Ts=None, fp=None)`

Write thread identifiers and stack traces to the file `fp`.

Parameters:
* `Ts`: the `Thread`s to dump; if unspecified use `threading.enumerate()`.
* `fp`: the file to which to write; if unspecified use `sys.stderr`.

## Class `TimingOutLock`

A `Lock` replacement which times out, used for locating deadlock points.

## Function `trace(*da, **dkw)`

Decorator to report the call and return of a function.

# Release Log



*Release 20240423*:
* Support "import *" by populating __all__ with X, r, s, TimingOutLock, thread_dump, stack_dump, trace.
* @trace: include the elapsed time on the return/exception log message.

*Release 20230613.1*:
Bugfix builtins monkey patch.

*Release 20230613*:
Honour $CS_DEBUG_BUILTINS envvar to monkey patch the builtins module, constraints via a white list.

*Release 20230610*:
* DebuggingRLock fixes.
* Move @trace from cs.py.func to cs.debug.
* Drop Lock and RLock alias factories - importers should just use the debugging lock classes directly.
* Rename threading.Thread to threading_Thread.
* Simplify the debugging lock classes.

*Release 20221118*:
stack_dump: cope when cs.logutils.setup_logging not run yet.

*Release 20211208*:
@trace moved to cs.pyfunc, other minor changes.

*Release 20200318*:
Remove use of cs.obj.O, universally supplanted by types.SimpleNamespace.

*Release 20181231*:
* New TimingOutLock for locating deadlock points, grew from debugging cs.vt.index.
* Other minor changes.

*Release 20171231*:
* Update imports for recentchanges.
* New context manager TraceSuite to trace start and end of a code suite.

*Release 20160918*:
selftest(): fix parameter ordering to match unittest.

*Release 20160828*:
Update metadata with "install_requires" instead of "requires".

*Release 20160827*:
* New openfiles() to return selected pathnames of open files via lsof(8).
* New selftest() to invoke unittests with benefits.
* DebugShell, a cmd.Cmd subclass for debugging - current use case calls this with self.__dict__ in a test case tearDwon.
* debug_object_shell: convenience wrapper for DebugShell to call it on an object's attributes.

*Release 20150116*:
PyPI prep.
