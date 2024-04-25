from mloggers import ConsoleLogger, Logger, OptionalLogger


def some_function(logger: Logger | None):
    opt_logger = OptionalLogger(logger)
    opt_logger.info("This will only log if the logger is not None.")


some_function(None)
some_function(ConsoleLogger())
