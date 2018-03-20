from django.db import models
from django.utils import timezone
from datetime import timedelta


class Weekly(models.Model):
    """Week summary object."""

    published_date = models.DateTimeField(blank=True, null=True)

    # Summary box
    week_name = models.CharField("name", max_length=200)
    week_started = models.DateField(default='2017-01-01')
    week_rate = models.DecimalField("rate", max_digits=3,
                                    decimal_places=2, default=0.0)
    time_tracked = models.DecimalField("time tracked", max_digits=5,
                                       decimal_places=2, default=0.0)
    highlights = models.TextField(blank=True)
    leaks = models.TextField(blank=True)

    # BuildUp Section, overall timing [!percents] [BuildUp.Main]
    bu_hi_time = models.IntegerField("Hi%", default=0)
    bu_mid_time = models.IntegerField("Mid%", default=0)
    bu_lo_time = models.IntegerField("Lo%", default=0)
    # [rid]bu_pc_time = models.IntegerField(default=0)

    # BuildUp Section, Maths. [BuildUp.Math]
    bu_math_time = models.DecimalField("Math", max_digits=5,
                                       decimal_places=2, default=0.00)
    bu_math_details = models.TextField("Math description", blank=True)

    # BuildUp Section, Computer Science. [BuildUp.CS]
    bu_cs_time = models.DecimalField("Computer Science", max_digits=5,
                                     decimal_places=2, default=0.0)
    bu_cs_details = models.TextField("CS description", blank=True)

    # BuildUp Section, Languages. [BuildUp.Lang]
    bu_lg_de_time = models.DecimalField("Deutsch", max_digits=5,
                                        decimal_places=2, default=0.0)
    bu_lg_fr_time = models.DecimalField("French", max_digits=5,
                                        decimal_places=2, default=0.0)
    bu_lg_jap_time = models.DecimalField("Japanese", max_digits=5,
                                         decimal_places=2, default=0.0)
    bu_lg_de_details = models.TextField("Deutsch details", blank=True)
    bu_lg_fr_details = models.TextField("French details", blank=True)
    bu_lg_jap_details = models.TextField("Japanese details", blank=True)

    # BuildUp Section, other (tech readings, feynman). [BuildUp.Others]
    bu_others_time = models.DecimalField("Others", max_digits=5,
                                         decimal_places=2, default=0.0)
    bu_others_details = models.TextField("Others details", blank=True)

    # OpK Section, Tourne [OpK.Tourne]
    opk_tourne_time = models.DecimalField("Tourne", max_digits=5,
                                          decimal_places=2, default=0.0)
    opk_tourne_details = models.TextField("Tourne details", blank=True)

    # OpK Section, GoBasquing [OpK.GoBasquing]
    opk_gobasquing_time = models.DecimalField("GoBasquing", max_digits=5,
                                              decimal_places=2, default=0.0)
    opk_gobasquing_details = models.TextField("GoBasquing details", blank=True)

    # OpK Section, Urgoiti [OpK.Urgoiti]
    opk_urgoiti_time = models.DecimalField("Urgoiti", max_digits=5,
                                           decimal_places=2, default=0.0)
    opk_urgoiti_details = models.TextField("Urgoiti details", blank=True)

    # OpK Section, other tours [OpK.Others]
    opk_other_tours_time = models.DecimalField("Other tours", max_digits=5,
                                               decimal_places=2, default=0.0)
    opk_other_tours_details = models.TextField("Other tours details",
                                               blank=True)

    # OpK Section, tries [OpK.Tries]
    opk_tries_time = models.DecimalField("Tries", max_digits=5,
                                         decimal_places=2, default=0.0)
    opk_tries_details = models.TextField("Tries details", blank=True)

    # OpK Section, design [Opk.Design] [not yet, but likely in the future]

    # KiC Section [KiC.Main]
    kic_time = models.DecimalField("KiC", max_digits=5, decimal_places=2,
                                   default=0.0)
    kic_details = models.TextField("KiC details", blank=True)

    # Stuff Box Section, Shared Time [StuffBox.Shared]
    stuff_shared_time = models.DecimalField("Shared Time", max_digits=5,
                                            decimal_places=2, default=0.0)
    stuff_shared_details = models.TextField("Shared Time details", blank=True)

    # Stuff Box Section, Ortu [StuffBox.Ortu]
    stuff_ortu_time = models.DecimalField("Ortu", max_digits=5,
                                          decimal_places=2, default=0.0)
    stuff_ortu_details = models.TextField("Ortu details", blank=True)

    # Stuff Box Section, Others [StuffBox.Others]
    stuff_others_time = models.DecimalField("Others", max_digits=5,
                                            decimal_places=2, default=0.0)
    stuff_others_details = models.TextField("Others details", blank=True)

    # Stuff Box Section, Sleep
    stuff_sleeping_time = models.DecimalField("Sleep", max_digits=5,
                                              decimal_places=2, default=0.0)
    # Stuff Box Section, junk stuff
    junk_stuff_time = models.DecimalField("Junk", max_digits=5,
                                          decimal_places=2, default=0.0)

    # Sport Section, overall features [Sport.Main]
    sport_intensity = models.IntegerField("Intensity", default=0)
    sport_cal = models.IntegerField("Calories", default=0)

    # Sport Section, running [Sport.Running]
    sport_run_time = models.DecimalField("Running time", max_digits=5,
                                         decimal_places=2, default=0.0)
    sport_run_dst = models.DecimalField("Distance", max_digits=5,
                                        decimal_places=2, default=0.0)
    sport_run_alt = models.IntegerField("Altitude", default=0)
    default_pace = timedelta(minutes=6)
    sport_run_pace = models.DurationField("Pace", default=default_pace)

    # Sport Section, biking [Sport.Bike]
    sport_bike_time = models.DecimalField("Bike time", max_digits=5,
                                          decimal_places=2, default=0.0)
    sport_bike_dst = models.DecimalField("Distance", max_digits=5,
                                         decimal_places=2, default=0.0)
    sport_bike_alt = models.IntegerField("Altitude", default=0)

    # Sport Section, others (surf, wallclimb...) [Sport.Others]
    sport_others_time = models.DecimalField("Other Sport", max_digits=5,
                                            decimal_places=2, default=0.0)
    sport_others_details = models.TextField("Other details", blank=True)

    def AwakeTime(self):
        """Calculate the hours awake."""
        sleep = self.stuff_sleeping_time
        at = (24 * 7) - sleep
        return at

    def BuCoreSum(self):
        """Sum all the BuildUp core hours."""
        math = self.bu_math_time
        cs = self.bu_cs_time
        core = math + cs
        return core

    def BuLgSum(self):
        """Sum all the language hours in a week."""
        de = self.bu_lg_de_time
        fr = self.bu_lg_fr_time
        jap = self.bu_lg_jap_time
        lang = de + fr + jap
        return lang

    def BuildUpSum(self):
        """Sum all the study hours in  week."""
        core = Weekly.BuCoreSum(self)
        lang = Weekly.BuLgSum(self)
        other = self.bu_others_time
        total = (core + lang) + other
        return total

    def BuPerc(self):
        """Return the study percentage w/ awake time."""
        at = Weekly.AwakeTime(self)
        bsum = Weekly.BuildUpSum(self)
        bu_perc = round((100 * bsum) / at, 2)
        return bu_perc

    def OpkSum(self):
        """Sum all the OpK hours in a week."""
        tourne = self.opk_tourne_time
        gobasquing = self.opk_gobasquing_time
        urgoiti = self.opk_urgoiti_time
        tries = self.opk_tries_time
        others = self.opk_other_tours_time
        opk_sum = (tourne +
                   gobasquing +
                   urgoiti +
                   tries +
                   others)
        return opk_sum

    def OpkPerc(self):
        """Return the OpK percentage w/ awake time."""
        at = Weekly.AwakeTime(self)
        opksum = Weekly.OpkSum(self)
        opk_perc = round((100 * opksum) / at, 2)
        return opk_perc

    def StuffSum(self):
        """Sum all the StuffBox hours in a week."""
        shared = self.stuff_shared_time
        ortu = self.stuff_ortu_time
        other = self.stuff_others_time
        stuff_sum = (shared + ortu + other)
        return stuff_sum

    def StuffPerc(self):
        """Return the StuffBox percentage w/ awake time."""
        at = Weekly.AwakeTime(self)
        stuffsum = Weekly.StuffSum(self)
        stuff_perc = round((100 * stuffsum) / at, 2)
        return stuff_perc

    def SportSum(self):
        """Sum all the Sport hours in a week."""
        run = self.sport_run_time
        bike = self.sport_bike_time
        other = self.sport_others_time
        sport_sum = (run + bike + other)
        return sport_sum

    def SportPerc(self):
        """Return the Sport percentage w/ awake time."""
        at = Weekly.AwakeTime(self)
        sportsum = Weekly.SportSum(self)
        sport_perc = round((100 * sportsum) / at, 2)
        return sport_perc

    def KicPerc(self):
        """Return the KiC percentage w/ awake time."""
        at = Weekly.AwakeTime(self)
        kic = self.kic_time
        kic_perc = round((100 * kic) / at, 2)
        return kic_perc

    def JunkPerc(self):
        """Return the KiC percentage w/ awake time."""
        at = Weekly.AwakeTime(self)
        junk = self.junk_stuff_time
        junk_perc = round((100 * junk) / at, 2)
        return junk_perc

    def WeekNumber(self):
        """Get the week number."""
        d = self.week_started
        week_no = d.isocalendar()
        return week_no[1]

    def UntrackedTime(self):
        """Calculate the amount of untracked time."""
        tt = self.time_tracked
        ut = (168 - tt)
        return ut

    def UntrackedTimePerc(self):
        """Calculate the perc of untracked time."""
        at = Weekly.AwakeTime(self)
        ut = Weekly.UntrackedTime(self)
        ut_perc = round((100 * ut) / at, 2)
        return ut_perc

    def publish(self):
        """Publish the week."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.week_name
