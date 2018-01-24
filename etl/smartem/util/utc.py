from datetime import datetime, tzinfo, timedelta


class UTC(tzinfo):
    """
    See https://aboutsimon.com/blog/2013/06/06/Datetime-hell-Time-zone-aware-to-UNIX-timestamp.html
    Somehow need to force timezone in....
    TODO: may use dateutil external package
    UTC
    """

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


utc = UTC()


def zulu_to_gmt(zulu_str):
    # input: 2016-05-31T15:55:33.2014241Z
    # iso_str : '2016-05-31T15:55:33GMT'
    iso_str = zulu_str.split('.')[0] + 'GMT'
    # timestamp = timegm(
    #         time.strptime(iso_str, '%Y-%m-%dT%H:%M:%SGMT')
    # )
    # print timestamp
    # print '-> %s' % datetime.utcfromtimestamp(timestamp).isoformat()

    return datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%SGMT').replace(tzinfo=utc)
