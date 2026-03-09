from pkg.helpers import helper


class Worker:
    def process(self):
        self.validate()
        helper()

    def validate(self):
        return True
