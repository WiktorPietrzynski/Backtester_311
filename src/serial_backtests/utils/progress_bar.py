


class ConsoleProgress:
    def __init__(self, limit: int, function_name: str = "") -> None:
        self.limit = limit
        self.function_name = function_name
        self.last_percent = 0
        self.last_iteration = 0
        self.sign = "█"
        self.bar_string = "_"
        print(f"{self.function_name} progress: 0% |{self.bar_string * 100}| 0/{self.limit}")

    def send(self, iteration: int) -> None:
        percent = int((iteration / self.limit) * 100)
        if percent != self.last_percent:
            bar = self.sign * percent
            bar_string = bar + self.bar_string * (100 - percent)
            self.last_percent = percent
            print(f"{self.function_name} progress: {percent}% |{bar_string}| {iteration}/{self.limit}")

    def append(self, next_iteration: int) -> None:
        self.last_iteration = last_iteration = self.last_iteration + next_iteration
        self.send(last_iteration)

def display_progress(function_name: str, limit: int, iteration: int) -> None:
    percent = int((iteration / limit) * 100)
    if percent > 100:
        percent = 100
    bar = "█" * percent
    bar_string = bar + "_" * (100 - percent)
    print(f"{function_name} progress: {percent}% |{bar_string}| {iteration}/{limit}")