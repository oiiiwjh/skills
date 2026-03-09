from pkg.helpers import helper
from pkg.models import Worker


def run_step():
    helper()


def main():
    worker = Worker()
    worker.process()
    run_step()
    unknown_callback()
