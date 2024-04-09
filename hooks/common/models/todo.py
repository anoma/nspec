from common.models.fileloc import FileLoc


class Todo(FileLoc):
    def __init__(self, path: str, line: int, col: int, message: str = ""):
        super().__init__(path, line, col)
        self.message = message

    def __str__(self):
        short_msg = (
            self.message[:100] + "..." if len(self.message) > 100 else self.message
        )
        location = super().__str__()
        return f"\033[92m{location}\033[0m \n - {short_msg}"

    def __repr__(self):
        return self.__str__()
