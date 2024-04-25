# This file is part of utils.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.
#

"""Utilities for measuring execution time.
"""

from __future__ import annotations

__all__ = ["logInfo", "timeMethod", "time_this"]

import datetime
import functools
import inspect
import logging
import time
from contextlib import contextmanager
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Iterable,
    Iterator,
    MutableMapping,
    Optional,
    Tuple,
)

from astropy import units as u

from .usage import _get_current_rusage, get_current_mem_usage, get_peak_mem_usage

if TYPE_CHECKING:
    from .logging import LsstLoggers


_LOG = logging.getLogger(__name__)


def _add_to_metadata(metadata: MutableMapping, name: str, value: Any) -> None:
    """Add a value to dict-like object, creating list as needed.

    The list grows as more values are added for that key.

    Parameters
    ----------
    metadata : `dict`-like, optional
        `dict`-like object that can store keys. Uses `add()` method if
        one is available, else creates list and appends value if needed.
    name : `str`
        The key to use in the metadata dictionary.
    value : Any
        Value to store in the list.
    """
    try:
        try:
            # PropertySet should always prefer LongLong for integers
            metadata.addLongLong(name, value)  # type: ignore
        except (TypeError, AttributeError):
            metadata.add(name, value)  # type: ignore
    except AttributeError:
        pass
    else:
        return

    # Fallback code where `add` is not implemented.
    if name not in metadata:
        metadata[name] = []
    metadata[name].append(value)


def _find_outside_stacklevel() -> int:
    """Find the stack level corresponding to caller code outside of this
    module.

    This can be passed directly to `logging.Logger.log()` to ensure
    that log messages are issued as if they are coming from caller code.

    Returns
    -------
    stacklevel : `int`
        The stack level to use to refer to a caller outside of this module.
        A ``stacklevel`` of ``1`` corresponds to the caller of this internal
        function and that is the default expected by `logging.Logger.log()`.

    Notes
    -----
    Intended to be called from the function that is going to issue a log
    message. The result should be passed into `~logging.Logger.log` via the
    keyword parameter ``stacklevel``.
    """
    stacklevel = 1  # the default for `Logger.log`
    for i, s in enumerate(inspect.stack()):
        module = inspect.getmodule(s.frame)
        if module is None:
            # Stack frames sometimes hang around so explicilty delete.
            del s
            continue
        if not module.__name__.startswith("lsst.utils"):
            # 0 will be this function.
            # 1 will be the caller which will be the default for `Logger.log`
            # and so does not need adjustment.
            stacklevel = i
            break
        # Stack frames sometimes hang around so explicilty delete.
        del s

    return stacklevel


def logPairs(
    obj: Any,
    pairs: Collection[Tuple[str, Any]],
    logLevel: int = logging.DEBUG,
    metadata: Optional[MutableMapping] = None,
    logger: Optional[logging.Logger] = None,
    stacklevel: Optional[int] = None,
) -> None:
    """Log ``(name, value)`` pairs to ``obj.metadata`` and ``obj.log``

    Parameters
    ----------
    obj : `object`
        An object with one or both of these two attributes:

        - ``metadata`` a `dict`-like container for storing metadata.
          Can use the ``add(name, value)`` method if found, else will append
          entries to a list.
        - ``log`` an instance of `logging.Logger` or subclass.

        If `None`, at least one of ``metadata`` or ``logger`` should be passed
        or this function will do nothing.
    pairs : sequence
        A sequence of ``(name, value)`` pairs, with value typically numeric.
    logLevel : `int, optional
        Log level (an `logging` level constant, such as `logging.DEBUG`).
    metadata : `collections.abc.MutableMapping`, optional
        Metadata object to write entries to.  Ignored if `None`.
    logger : `logging.Logger`
        Log object to write entries to.  Ignored if `None`.
    stacklevel : `int`, optional
        The stack level to pass to the logger to adjust which stack frame
        is used to report the file information. If `None` the stack level
        is computed such that it is reported as the first package outside
        of the utils package. If a value is given here it is adjusted by
        1 to account for this caller.
    """
    if obj is not None:
        if metadata is None:
            try:
                metadata = obj.metadata
            except AttributeError:
                pass
        if logger is None:
            try:
                logger = obj.log
            except AttributeError:
                pass
    strList = []
    for name, value in pairs:
        if metadata is not None:
            _add_to_metadata(metadata, name, value)
        strList.append(f"{name}={value}")
    if logger is not None:
        # Want the file associated with this log message to be that
        # of the caller. This is expensive so only do it if we know the
        # message will be issued.
        timer_logger = logging.getLogger("timer." + logger.name)
        if timer_logger.isEnabledFor(logLevel):
            if stacklevel is None:
                stacklevel = _find_outside_stacklevel()
            else:
                # Account for the caller stack.
                stacklevel += 1
            timer_logger.log(logLevel, "; ".join(strList), stacklevel=stacklevel)


def logInfo(
    obj: Any,
    prefix: str,
    logLevel: int = logging.DEBUG,
    metadata: Optional[MutableMapping] = None,
    logger: Optional[logging.Logger] = None,
    stacklevel: Optional[int] = None,
) -> None:
    """Log timer information to ``obj.metadata`` and ``obj.log``.

    Parameters
    ----------
    obj : `object`
        An object with both or one these two attributes:

        - ``metadata`` a `dict`-like container for storing metadata.
          Can use the ``add(name, value)`` method if found, else will append
          entries to a list.
        - ``log`` an instance of `logging.Logger` or subclass.

        If `None`, at least one of ``metadata`` or ``logger`` should be passed
        or this function will do nothing.
    prefix : `str`
        Name prefix, the resulting entries are ``CpuTime``, etc.. For example
        `timeMethod` uses ``prefix = Start`` when the method begins and
        ``prefix = End`` when the method ends.
    logLevel : optional
        Log level (a `logging` level constant, such as `logging.DEBUG`).
    metadata : `collections.abc.MutableMapping`, optional
        Metadata object to write entries to, overriding ``obj.metadata``.
    logger : `logging.Logger`
        Log object to write entries to, overriding ``obj.log``.
    stacklevel : `int`, optional
        The stack level to pass to the logger to adjust which stack frame
        is used to report the file information. If `None` the stack level
        is computed such that it is reported as the first package outside
        of the utils package. If a value is given here it is adjusted by
        1 to account for this caller.

    Notes
    -----
    Logged items include:

    - ``Utc``: UTC date in ISO format (only in metadata since log entries have
      timestamps).
    - ``CpuTime``: System + User CPU time (seconds). This should only be used
        in differential measurements; the time reference point is undefined.
    - ``MaxRss``: maximum resident set size. Always in bytes.

    All logged resource information is only for the current process; child
    processes are excluded.

    The metadata will be updated with a ``__version__`` field to indicate the
    version of the items stored. If there is no version number it is assumed
    to be version 0.

    * Version 0: ``MaxResidentSetSize`` units are platform-dependent.
    * Version 1: ``MaxResidentSetSize`` will be stored in bytes.
    """
    if metadata is None and obj is not None:
        try:
            metadata = obj.metadata
        except AttributeError:
            pass
    if metadata is not None:
        # Log messages already have timestamps.
        utcStr = datetime.datetime.utcnow().isoformat()
        _add_to_metadata(metadata, name=prefix + "Utc", value=utcStr)

        # Force a version number into the metadata.
        # v1: Ensure that max_rss field is always bytes.
        metadata["__version__"] = 1
    if stacklevel is not None:
        # Account for the caller of this routine not knowing that we
        # are going one down in the stack.
        stacklevel += 1

    usage = _get_current_rusage()
    logPairs(
        obj=obj,
        pairs=[(prefix + k[0].upper() + k[1:], v) for k, v in usage.dict().items()],
        logLevel=logLevel,
        metadata=metadata,
        logger=logger,
        stacklevel=stacklevel,
    )


def timeMethod(
    _func: Optional[Any] = None,
    *,
    metadata: Optional[MutableMapping] = None,
    logger: Optional[logging.Logger] = None,
    logLevel: int = logging.DEBUG,
) -> Callable:
    """Measure duration of a method.

    Parameters
    ----------
    func
        The method to wrap.
    metadata : `collections.abc.MutableMapping`, optional
        Metadata to use as override if the instance object attached
        to this timer does not support a ``metadata`` property.
    logger : `logging.Logger`, optional
        Logger to use when the class containing the decorated method does not
        have a ``log`` property.
    logLevel : `int`, optional
        Log level to use when logging messages. Default is `~logging.DEBUG`.

    Notes
    -----
    Writes various measures of time and possibly memory usage to the
    metadata; all items are prefixed with the function name.

    .. warning::

       This decorator only works with instance methods of any class
       with these attributes:

       - ``metadata``: an instance of `collections.abc.Mapping`. The ``add``
         method will be used if available, else entries will be added to a
         list.
       - ``log``: an instance of `logging.Logger` or subclass.

    Examples
    --------
    To use:

    .. code-block:: python

        import lsst.utils as utils
        import lsst.pipe.base as pipeBase
        class FooTask(pipeBase.Task):
            pass

            @utils.timeMethod
            def run(self, ...): # or any other instance method you want to time
                pass
    """

    def decorator_timer(func: Callable) -> Callable:
        @functools.wraps(func)
        def timeMethod_wrapper(self: Any, *args: Any, **keyArgs: Any) -> Any:
            # Adjust the stacklevel to account for the wrappers.
            # stacklevel 1 would make the log message come from this function
            # but we want it to come from the file that defined the method
            # so need to increment by 1 to get to the caller.
            stacklevel = 2
            logInfo(
                obj=self,
                prefix=func.__name__ + "Start",
                metadata=metadata,
                logger=logger,
                logLevel=logLevel,
                stacklevel=stacklevel,
            )
            try:
                res = func(self, *args, **keyArgs)
            finally:
                logInfo(
                    obj=self,
                    prefix=func.__name__ + "End",
                    metadata=metadata,
                    logger=logger,
                    logLevel=logLevel,
                    stacklevel=stacklevel,
                )
            return res

        return timeMethod_wrapper

    if _func is None:
        return decorator_timer
    else:
        return decorator_timer(_func)


@contextmanager
def time_this(
    log: Optional[LsstLoggers] = None,
    msg: Optional[str] = None,
    level: int = logging.DEBUG,
    prefix: Optional[str] = "timer",
    args: Iterable[Any] = (),
    mem_usage: bool = False,
    mem_child: bool = False,
    mem_unit: u.Quantity = u.byte,
    mem_fmt: str = ".0f",
) -> Iterator[None]:
    """Time the enclosed block and issue a log message.

    Parameters
    ----------
    log : `logging.Logger`, optional
        Logger to use to report the timer message. The root logger will
        be used if none is given.
    msg : `str`, optional
        Context to include in log message.
    level : `int`, optional
        Python logging level to use to issue the log message. If the
        code block raises an exception the log message will automatically
        switch to level ERROR.
    prefix : `str`, optional
        Prefix to use to prepend to the supplied logger to
        create a new logger to use instead. No prefix is used if the value
        is set to `None`. Defaults to "timer".
    args : iterable of any
        Additional parameters passed to the log command that should be
        written to ``msg``.
    mem_usage : `bool`, optional
        Flag indicating whether to include the memory usage in the report.
        Defaults, to False.
    mem_child : `bool`, optional
        Flag indication whether to include memory usage of the child processes.
    mem_unit : `astropy.units.Unit`, optional
        Unit to use when reporting the memory usage. Defaults to bytes.
    mem_fmt : `str`, optional
        Format specifier to use when displaying values related to memory usage.
        Defaults to '.0f'.
    """
    if log is None:
        log = logging.getLogger()
    if prefix:
        log_name = f"{prefix}.{log.name}" if not isinstance(log, logging.RootLogger) else prefix
        log = logging.getLogger(log_name)

    success = False
    start = time.time()
    if mem_usage:
        current_usages_start = get_current_mem_usage()
        peak_usages_start = get_peak_mem_usage()

    try:
        yield
        success = True
    finally:
        end = time.time()

        # The message is pre-inserted to allow the logger to expand
        # the additional args provided. Make that easier by converting
        # the None message to empty string.
        if msg is None:
            msg = ""

        # Convert user provided parameters (if any) to mutable sequence to make
        # mypy stop complaining when additional parameters will be added below.
        params = list(args) if args else []

        if not success:
            # Something went wrong so change the log level to indicate
            # this.
            level = logging.ERROR

        # Specify stacklevel to ensure the message is reported from the
        # caller (1 is this file, 2 is contextlib, 3 is user)
        params += (": " if msg else "", end - start)
        msg += "%sTook %.4f seconds"
        if mem_usage and log.isEnabledFor(level):
            current_usages_end = get_current_mem_usage()
            peak_usages_end = get_peak_mem_usage()

            current_deltas = [end - start for end, start in zip(current_usages_end, current_usages_start)]
            peak_deltas = [end - start for end, start in zip(peak_usages_end, peak_usages_start)]

            current_usage = current_usages_end[0]
            current_delta = current_deltas[0]
            peak_delta = peak_deltas[0]
            if mem_child:
                current_usage += current_usages_end[1]
                current_delta += current_deltas[1]
                peak_delta += peak_deltas[1]

            if not mem_unit.is_equivalent(u.byte):
                _LOG.warning("Invalid memory unit '%s', using '%s' instead", mem_unit, u.byte)
                mem_unit = u.byte

            msg += (
                f"; current memory usage: {current_usage.to(mem_unit):{mem_fmt}}"
                f", delta: {current_delta.to(mem_unit):{mem_fmt}}"
                f", peak delta: {peak_delta.to(mem_unit):{mem_fmt}}"
            )
        log.log(level, msg, *params, stacklevel=3)
