import cmd
from sys import argv
from oldschool_management_tools.calendar_tools import parse_day, CalendarReader
from oldschool_management_tools.calendar_integrator import CalendarIntegrator, OutlookIntegrator, ParquetIntegrator, DumpingOutlookIntegrator


class MgmtToolsCmd(cmd.Cmd):
    intro = "Welcome to Old School Management Tools"
    prompt = "(mgmt) "

    def __init__(self, integrator: CalendarIntegrator):
        super(MgmtToolsCmd, self).__init__()
        self.calendar_reader = CalendarReader(integrator)

    def do_prompt_tasks(self, day):
        parsed_day = parse_day(day)
        self.calendar_reader.prompt_day_tasks(parsed_day)

    def do_show_sched(self, day):
        parsed_day = parse_day(day)
        self.calendar_reader.show_day_sched(parsed_day)

    def do_fill_prep(self, day):
        parsed_day = parse_day(day)
        self.calendar_reader.fill_prep(parsed_day)

    def do_wipe_prep(self, day):
        parsed_day = parse_day(day)
        self.calendar_reader.wipe_prep(parsed_day)

    @staticmethod
    def do_die(args):
        return True

    @staticmethod
    def do_exit(args):
        return True

    @staticmethod
    def do_EOF(args):
        return True


def run():
    if len(argv) == 1:
        integrator = OutlookIntegrator()
    elif argv[1] == "parquet":
        parq_file = argv[2]
        integrator = ParquetIntegrator(parq_file)
    elif argv[1] == "dump":
        integrator = DumpingOutlookIntegrator(argv[2])
    else:
        print(f"Bad input {argv[1]}")
        exit(1)
    MgmtToolsCmd(integrator).cmdloop()
    exit(0)
