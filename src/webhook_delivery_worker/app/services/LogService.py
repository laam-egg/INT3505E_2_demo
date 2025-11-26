import time
import traceback

class LogService:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def log(self, msg: str) -> None:
        """
        Prints date, time and log prefix before the message.
        """
        print(f"[{self.prefix}] {time.strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

    def info(self, msg: str) -> None:
        return self.log(f"[INFO] {msg}")
    
    def error(self, msg: str) -> None:
        return self.log(f"[ERROR] {msg}")
    
    def debug(self, msg: str) -> None:
        return self.log(f"[DEBUG] {msg}")
    
    def exception(self) -> None:
        """
        Logs the entire stack trace. Use traceback.format_exc().
        """
        stack_trace = traceback.format_exc()
        return self.log(f"[EXCEPTION] {stack_trace}")
