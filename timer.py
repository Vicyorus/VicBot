def GetInHMS(seconds, hms, value):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    if value == 3:
        return hms % (hours, minutes, seconds)
    elif value == 2:
        return hms % (minutes, seconds)


def seen(user, seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    if hours == 1:
        hrs = "hour"
    else:
        hrs = "hours"
    if seconds == 1:
        scs = "second"
    else:
        scs = "seconds"
    if minutes == 1:
        mns = "minute"
    else:
        mns = "minutes"

    if hours == 0 and minutes == 0 and seconds != 0:
        return "I last saw %s %d %s ago." % (user, seconds, scs)
    elif hours == 0 and minutes != 0 and seconds == 0:
        return "I last saw %s %d %s ago." % (user, minutes, mns)
    elif hours != 0 and minutes == 0 and seconds == 0:
        return "I last saw %s %d %s ago." % (user, hours, hrs)
    elif hours == 0 and minutes != 0 and seconds != 0:
        return "I last saw %s %d %s and %d %s ago." % (user, minutes, mns, seconds, scs)
    elif hours != 0 and minutes != 0 and seconds != 0:
        return "I last saw %s %d %s, %d %s and %d %s ago." % (user, hours, hrs, minutes, mns, seconds, scs)
    elif hours != 0 and minutes == 0 and seconds != 0:
        return "I last saw %s %d %s and %d %s ago." % (user, hours, hrs, seconds, scs)
    elif hours != 0 and minutes != 0 and seconds == 0:
        return "I last saw %s %d %s and %d %s ago." % (user, hours, hrs, minutes, mns)
