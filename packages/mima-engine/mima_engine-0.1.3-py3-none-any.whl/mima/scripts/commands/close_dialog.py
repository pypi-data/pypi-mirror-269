from ..command import Command


class CommandCloseDialog(Command):
    def start(self):
        self.engine.dialog_active = False
        self.engine.exit_dialog_active = False
        self.completed = True
