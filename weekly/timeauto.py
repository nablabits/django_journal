"""Automatize the time dbentries by collecting the data from the backup."""

import os
import re
import shutil
import records
from datetime import date, timedelta, datetime
from zipfile import ZipFile
from .models import Weekly
from django.utils import timezone


class TrackDB(object):
    """Get the last db file & unpack it into a tmp folder."""

    def GetPath(self):
        """Select te path to the db file. Try first default."""
        default = '/home/davif/Dropbox/Aplicaciones/Swipetimes Time Tracker/'
        zip_dir = os.path.isdir(default)
        while zip_dir is False:
            default = input('Couldn\'t find that location, choose manually: ')
            zip_dir = os.path.isdir(default)
        return default

    def GetFile(self):
        """Get the last zip file from the path."""
        path = self.GetPath()
        file_namelist = []
        file_timelist = []
        for entry in os.scandir(path):
            if re.search(r'.zip', entry.name):
                file_timelist.append(entry.stat().st_mtime)
                file_namelist.append(entry.name)
        max_idx = file_timelist.index(max(file_timelist))
        zipfile = file_namelist[max_idx]
        return zipfile

    def FileCheck(self):
        """Check if the zip is already extracted."""
        # first, check if folder exists
        zip_path = self.GetPath()
        tmp = zip_path + 'tmp/'
        if os.path.isdir(tmp):
            zipfile = self.GetPath() + self.GetFile()
            zipfile_creation = os.stat(zipfile).st_mtime
            folder_creation = os.stat(tmp).st_mtime
            # Now compare creation dates
            if folder_creation > zipfile_creation:
                # The folder is the most recent element, so we have the last
                # version extracted
                print('Previous file detected')
                exists = True
            else:
                # The folder is not the most recent element, so we have a
                # newer file to extract.
                exists = False
        else:
            # The folder doesn't exist, so we have to extract the file
            exists = False

        return exists

    def GetDB(self):
        """Extract the DB into a temporally folder."""
        # fist, check if the file alredy exists
        checkfile = self.FileCheck()
        path = self.GetPath()
        tmp_path = self.GetPath() + 'tmp/'
        if checkfile is True:
            # File already existed
            files_in_path = os.listdir(tmp_path)
            if len(files_in_path) > 1:
                print(files_in_path)
                raise ValueError('more than one file in dir')
            dbfile = tmp_path + files_in_path[0]
        else:
            # There is not folder yet.
            zipfile = path + self.GetFile()
            print('origin:', zipfile)
            tmp = self.GetPath() + 'tmp/'
            with ZipFile(zipfile) as zip_file:
                members = zip_file.namelist()
                if len(members) > 1:
                    raise ValueError('more than one entry in the zip file')
                zip_file.extract(members[0], path=tmp)
                print('File found & extracted to tmp folder')
            dbfile = tmp + members[0]
        return dbfile

    def CleanUp(self):
        """Clean de tmp dir after use."""
        tmp_path = self.GetPath() + 'tmp/'
        shutil.rmtree(tmp_path)
        print('tmp folder deleted once used')


class DataQueries(object):
    """Once got the file, extract the data to fill in the fields."""

    def SelectWeek():
        """Choose the week from where data will be imported."""
        # first, determine last sunday
        today = date.today()
        delta = timedelta(days=-1)
        last = today

        if last.isocalendar()[2] == 7:
            print('Warning! will be used this week.')

        # reduce days until reach sunday
        while last.isocalendar()[2] != 7:
            last = last + delta

        first = last

        # reduce days until reach monday
        while first.isocalendar()[2] != 1:
            first = first + delta
        accept = input('Will be used: ' + str(first) + ' to ' + str(last) +
                       '[q to abort] ]: ')

        if accept == 'q':
            raise KeyboardInterrupt('The process was stopped by user.')

        week_range = (first, last)
        return week_range

    tdb = TrackDB()
    zipfile = tdb.GetDB()
    db = records.Database('sqlite:///' + zipfile)
    week_range = SelectWeek()
    project_range = range(19, 39)

    week_filter = ("date(started) BETWEEN\'" + str(week_range[0]) +
                   "\' AND \'" + str(week_range[1]) + "\'")

    all_times = db.query("SELECT * FROM work WHERE " + week_filter)

    # Iterator to get all different queries
    project_sums = {}
    count = 0
    for project in project_range:
        count += 1
        project = str(project)
        query = db.query("SELECT * FROM work WHERE " + week_filter +
                         " AND project = \'" + project + "\'")

        # Sum all the times
        total = 0
        for row in query:
            count += 1
            start = datetime.strptime(row.started, '%Y-%m-%d %H:%M:%S')
            end = row.stopped
            if not end:
                end = datetime.now()
            else:
                end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

            diff = (end.timestamp() - start.timestamp()) / 3600  # in hours
            total = round(total + diff, 1)

        # Update the dict
        project_sums[project] = total

    # Debug
    # for i in sorted(project_sums):
    #     print(i, '=>', project_sums[i])
    # print(count, 'loops')

    # BuildUp Hours this week query (for Quality percents)
    bu_data = db.query("SELECT * FROM work WHERE " + week_filter +
                       "AND project BETWEEN 19 AND 24")

    # Quality time {tags 6(mid), 7(hi) & 8(lo)]}
    hi, mid, lo = '7', '6', '8'
    common = ('SELECT started, stopped FROM work ' +
              'INNER JOIN work_tag ON work.id=work_id ' +
              'WHERE work_tag.tag_id = ')
    qlt_hi_data = db.query(common + hi + ' AND ' + week_filter)
    qlt_mid_data = db.query(common + mid + ' AND ' + week_filter)
    qlt_lo_data = db.query(common + lo + ' AND ' + week_filter)


class WeekOutcomes(object):
    """Fiddle the queries to get values for the db."""

    weekqueries = DataQueries()

    def SumTimes(self, df):
        """Sum all the times given by the db query."""
        total = 0
        for row in df:
            start = datetime.strptime(row.started, '%Y-%m-%d %H:%M:%S')
            end = row.stopped
            if not end:
                end = datetime.now()
            else:
                end = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

            diff = (end.timestamp() - start.timestamp()) / 3600  # in hours
            total = round(total + diff, 1)
        return total

    def QualityPerc(self, data):
        """Qualtiy Percents are calculated over BuildUp Time."""
        bu_time = self.SumTimes(self.weekqueries.bu_data)
        data = self.SumTimes(data)
        if bu_time == 0:  # Avoid division by 0
            result = 0
        else:
            result = round(100 * data / bu_time, 0)
        return result

    def TimeTracked(self):
        """Calculate the time tracked."""
        df = self.weekqueries.all_times
        result = round(self.SumTimes(df), 2)
        return result

    def Values(self):
        """Create a dict with all the Values for the db."""
        fields = {}
        df = self.weekqueries

        # Main
        fields['week_name'] = 'Autoextracted by app'
        fields['week_started'] = df.week_range[0]
        fields['time_tracked'] = self.TimeTracked()

        # BuildUp Percents
        fields['bu_hi_time'] = self.QualityPerc(df.qlt_hi_data)
        fields['bu_mid_time'] = self.QualityPerc(df.qlt_mid_data)
        fields['bu_lo_time'] = self.QualityPerc(df.qlt_lo_data)

        # BuildUp times
        fields['bu_math_time'] = df.project_sums['19']
        fields['bu_cs_time'] = df.project_sums['20']
        fields['bu_lg_de_time'] = df.project_sums['21']
        fields['bu_lg_fr_time'] = df.project_sums['22']
        fields['bu_lg_jap_time'] = df.project_sums['23']
        fields['bu_others_time'] = df.project_sums['24']

        # OpK times
        fields['opk_tourne_time'] = df.project_sums['26']
        fields['opk_gobasquing_time'] = df.project_sums['27']
        fields['opk_urgoiti_time'] = df.project_sums['30']
        fields['opk_other_tours_time'] = df.project_sums['29']
        fields['opk_tries_time'] = df.project_sums['28']

        # KiC times
        fields['kic_time'] = df.project_sums['25']

        # StuffBox times
        fields['stuff_shared_time'] = df.project_sums['31']
        fields['stuff_ortu_time'] = df.project_sums['32']
        fields['stuff_others_time'] = df.project_sums['33']

        fields['stuff_sleeping_time'] = df.project_sums['38']
        fields['junk_stuff_time'] = df.project_sums['37']

        return fields

    def insert(self):
        """Insert the data into the db."""
        field = self.Values()
        Weekly.objects.create(week_name=field['week_name'],
                              week_started=field['week_started'],
                              time_tracked=field['time_tracked'],
                              bu_math_time=field['bu_math_time'],
                              bu_cs_time=field['bu_cs_time'],
                              bu_lg_de_time=field['bu_lg_de_time'],
                              bu_lg_fr_time=field['bu_lg_fr_time'],
                              bu_lg_jap_time=field['bu_lg_jap_time'],
                              bu_hi_time=field['bu_hi_time'],
                              bu_mid_time=field['bu_mid_time'],
                              bu_lo_time=field['bu_lo_time'],
                              bu_others_time=field['bu_others_time'],
                              opk_tourne_time=field['opk_tourne_time'],
                              opk_gobasquing_time=field['opk_gobasquing_time'],
                              opk_urgoiti_time=field['opk_urgoiti_time'],
                              opk_other_tours_time=field['opk_other_tours_time'],
                              opk_tries_time=field['opk_tries_time'],
                              kic_time=field['kic_time'],
                              stuff_shared_time=field['stuff_shared_time'],
                              stuff_ortu_time=field['stuff_ortu_time'],
                              stuff_others_time=field['stuff_others_time'],
                              stuff_sleeping_time=field['stuff_sleeping_time'],
                              junk_stuff_time=field['junk_stuff_time'],
                              published_date=timezone.now()
                              )
        print('New entry added')

DataQueries()

data = WeekOutcomes()
fields = data.Values()
for k, v in fields.items():
    print(k, v)

data.insert()

tdb = TrackDB()
tdb.CleanUp()
