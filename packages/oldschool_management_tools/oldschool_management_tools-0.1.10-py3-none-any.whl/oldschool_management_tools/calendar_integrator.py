from oldschool_management_tools.calendar_items.calendar_item import CalendarItem
from datetime import datetime, timedelta
import os
import pandas as pd
if os.name == "nt":
    from win32com import client


class CalendarIntegrator:

    def __init__(self):
        self.PREP_DURATION = 15
    
    def get_calendar(self, begin, end):
        pass
    
    def get_day_cal(self, cal_date: datetime):
        pass
    
    def add_apt(self, apt: CalendarItem):
        pass

    def delete_cal_item(self, cal_date: datetime, apt: CalendarItem):
        pass


class OutlookIntegrator(CalendarIntegrator):
    
    def __init__(self):
        super().__init__()
        self.outlook = client.Dispatch('Outlook.Application')
    
    def get_calendar(self, begin, end):
        mapi = self.outlook.GetNamespace('MAPI')
        calendar = mapi.getDefaultFolder(9).Items
        calendar.IncludeRecurrences = True
        calendar.Sort('[Start]')

        restriction = "[Start] >= '" + begin.strftime('%d/%m/%Y') + "' AND [END] <= '" + end.strftime(
            '%d/%m/%Y') + "'"
        calendar = calendar.Restrict(restriction)
        return calendar

    def get_day_cal(self, cal_date: datetime):
        apts = self.get_calendar(cal_date, cal_date + timedelta(days=1))
        return [CalendarItem.from_outlook_apt(apt) for apt in apts]

    def add_apt(self, apt: CalendarItem):
        appt = self.outlook.CreateItem(1)
        appt.Start = str(apt.start_datetime)[0:-6]
        appt.Subject = apt.name
        appt.Categories = apt.category + " Category"
        appt.Duration = self.PREP_DURATION
        appt.Location = apt.location
        appt.Save()
        return appt

    def delete_cal_item(self, cal_date: datetime, apt: CalendarItem):
        outl_apts = self.get_calendar(cal_date, cal_date + timedelta(days=1))
        for outl_apt in outl_apts:
            if CalendarItem.from_outlook_apt(outl_apt) == apt:
                outl_apt.Delete()
                return


class DumpingOutlookIntegrator(OutlookIntegrator):

    def __init__(self, dump_dir):
        super().__init__()
        self.dump_dir = dump_dir
        self.dump_index = 0
        os.mkdir(dump_dir)

    def get_day_cal(self, cal_date: datetime):
        result = super().get_day_cal(cal_date)
        self.dump_items(result, "get_day_cal")
        return result

    def add_apt(self, apt: CalendarItem):
        result = super().add_apt(apt)
        self.dump_items([result], "add_apt")
        return result

    def dump_items(self, items, function_called):
        df = pd.DataFrame(data=items)
        df.to_parquet(f"{self.dump_dir}/{function_called}-{self.dump_index}.parquet")
        self.dump_index += 1

    def delete_cal_item(self, cal_date: datetime, apt: CalendarItem):
        super().delete_cal_item(cal_date, apt)


class ParquetIntegrator(CalendarIntegrator):

    def __init__(self, input_file):
        super().__init__()
        self.df = pd.read_parquet(input_file)
        self.items = self.df.apply(lambda row: CalendarItem(*row), axis=1).tolist()

    def get_calendar(self, begin, end):
        return self.items

    def get_day_cal(self, cal_date: datetime):
        return self.get_calendar(cal_date, cal_date + timedelta(days=1))

    def add_apt(self, apt: CalendarItem):
        self.items.append(apt)
        self.items.sort(key=lambda x: x.start_datetime)
        return

    def delete_cal_item(self, cal_date: datetime, apt: CalendarItem):
        self.items.remove(apt)
