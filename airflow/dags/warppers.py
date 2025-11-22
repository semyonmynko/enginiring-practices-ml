from airflow.exceptions import AirflowFailException


def task_safe(func):
    """Decorator for safe Airflow task execution"""

    def wrapper(self, **context):
        self.logger.info(f"Starting task: {func.__name__}")
        try:
            result = func(self, **context)
            self.logger.info(f"Task {func.__name__} completed successfully.")
            return result

        except FileNotFoundError as e:
            self.logger.error(f"File not found: {e}")
            raise AirflowFailException(
                f"Critical error in {func.__name__}: missing file"
            )

        except UnicodeDecodeError as e:
            self.logger.warning(f"Encoding issue: {e}")
            raise Exception("Encoding error - retry may help")

        except ConnectionError as e:
            self.logger.warning(f"Network issue: {e}")
            raise AirflowFailException("Network temporarily unavailable")

        except ValueError as e:
            self.logger.error(f"Invalid data: {e}")
            raise AirflowFailException(f"Data validation failed in {func.__name__}")

        except TypeError as e:
            self.logger.error(f"Invalid data: {e}")
            raise AirflowFailException(f"Data validation failed in {func.__name__}")

        except Exception as e:
            self.logger.exception(f"Unexpected error in {func.__name__}: {e}")
            raise

    return wrapper
