from weekly.models import Weekly
from incomes.models import Customer, Hour, Income
from rest_framework import serializers


class WeeklySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weekly
        fields = ('week_name', 'week_started', 'week_rate', 'time_tracked',
                  'highlights', 'leaks', 'bu_hi_time', 'bu_mid_time',
                  'bu_lo_time', 'bu_math_time', 'bu_math_details',
                  'bu_cs_time', 'bu_cs_details', 'bu_lg_de_time',
                  'bu_lg_fr_time', 'bu_lg_jap_time', 'bu_lg_de_details',
                  'bu_lg_fr_details', 'bu_lg_jap_details',
                  'bu_others_time', 'bu_others_details', 'opk_tourne_time',
                  'opk_tourne_details', 'opk_gobasquing_time',
                  'opk_gobasquing_details', 'opk_urgoiti_time',
                  'opk_urgoiti_details', 'opk_other_tours_time',
                  'opk_other_tours_details', 'opk_tries_time',
                  'opk_tries_details', 'kic_time', 'kic_details',
                  'stuff_shared_time', 'stuff_shared_details',
                  'stuff_ortu_time', 'stuff_ortu_details', 'stuff_others_time',
                  'stuff_others_details', 'stuff_sleeping_time',
                  'junk_stuff_time', 'sport_intensity', 'sport_cal',
                  'sport_run_time', 'sport_run_dst', 'sport_run_alt',
                  'sport_run_pace', 'sport_bike_dst', 'sport_bike_time',
                  'sport_bike_alt', 'sport_others_time',
                  'sport_others_details',)


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields=('date', 'name', 'comments')


class IncomesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        who = serializers.HyperlinkedRelatedField(
            read_only=True, view_name='income-detail')

        model = Income
        fields=('date', 'who', 'cash', 'tip', 'comments')


class HoursSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        who = serializers.HyperlinkedRelatedField(
            read_only=True, view_name='income-detail')

        model = Hour
        fields=('who', 'dedication', 'month', 'comments')
