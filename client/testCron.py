from crontab import CronTab
from crontab import CronSlices

def cronHandler(data):
    if not data:
        return
    s = data.split(':')
    cronCommand = s[1].strip()
    if cronCommand not in ["on", "off"]:
        print("Cron command invalid, should be 'on' or 'off'. Command: %s" % cronCommand)
        return

    cronString = s[2].strip()
    if not CronSlices.is_valid(cronString):
        print("Cron time string invalid. Time string: %s" % cronString)
        return
    
    # Now we've validated the command, set a cron job
    cron_file = CronTab(user=True)
    it = cron_file.find_command(cronCommand)
    try:
        job = it.next()
        print("Found existing cron task for %s" % cronCommand)
    except StopIteration:
        job = cron_file.new(command="echo %s >> /tmp/test.txt" % cronCommand)
        print("Creating new cron task for %s" % cronCommand)

    job.setall(cronString)
    job.enable()
    cron_file.write()
