"""
This module implements a format handler that writes log data into
a very basis HTML format, useful for readable reports. There is not
a corresponding parser
"""
import divelog

FORMAT_NAME = 'HTML'


def parse(file):
    raise NotImplementedError()


def __open(file, name, classes=None, attributes=None):
    file.write('<%s' % name)
    if classes:
        file.write(' class="%s"' % classes)
    if attributes:
        for key in attributes:
            file.write(' %s="%s"' % (key, attributes[key]))
    file.write('>')


def __close(file, name):
    file.write('</%s>' % name)


def __opened(file, name, attributes):
    file.write('<%s' % name)
    for key in attributes:
        file.write(' %s="%s"' % (key, attributes[key]))
    file.write('>')
    

def __node(file, name, value, classes=None):
    __open(file, name, classes)
    file.write(value)
    __close(file, name)


def __label(file, value, classes=None):
    __node(file, 'label', value, classes)


def __labeled(file, label, value):
    __open(file, 'div', 'row')
    __open(file, 'div', 'col-md-2')
    __label(file, label)
    __close(file, 'div')    
    __open(file, 'div', 'col-md-10')
    file.write(value)
    __close(file, 'div')
    __close(file, 'div')
    

def __topen(file, headings=None, classes=None):
    __open(file, 'table', classes)
    __open(file, 'thead')
    if headings:
        __open(file, 'tr')
        for heading in headings:
            __node(file, 'th', heading)
        __close(file, 'tr')
    __close(file, 'thead')
    __open(file, 'tbody')


def __trow(file, data):
    __open(file, 'tr')
    for datum in data:
        __node(file, 'td', datum)
    __close(file, 'tr')


def __tclose(file):
    __close(file, 'tbody')
    __close(file, 'table')


def dump(log, file):
    """
    Serialize the log to the provided file object.
    """
    ts_format = '%A, %d. %B %Y %I:%M%p'

    file.write('<!DOCTYPE html>')
    __open(file, 'html', attributes={'lang': 'en'})
    __open(file, 'head')

    __opened(file, 'meta', {'charset': 'utf-8'})
    __opened(file, 'meta', 
             {'http-equiv': 'X-UA-Compatible', 'content': 'IE=edge'}) 
    __opened(file, 'meta', 
             {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'})

    __node(file, 'title', 'Dive Log')

    file.write('<link rel="stylesheet" ' +
               'href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/' +
               'bootstrap.min.css" ' +
               'integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdj' +
               'ZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymousOD">')
    file.write('<link rel="stylesheet" ' +
               'href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/' +
               'bootstrap-theme.min.css" ' +
               'integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn' +
               '3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">')
    file.write('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6' +
               '/js/bootstrap.min.js" ' +
               'integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELq' +
               'xss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>')

    __close(file, 'head')
    __open(file, 'body')

    __node(file, 'h1', 'Dive Log')

    if log.computer_model:
        __open(file, 'div', 'container')
        __labeled(file, 'Computer Model', log.computer_model)
        __labeled(file, 'Serial Number', log.computer_serial)
        __close(file, 'div')

    for dive in log.dives:
        __node(file, 'h2', 'Dive Number %s' % dive.sequence_number)
        __open(file, 'div', 'container')
        dt = dive.leave_surface_time
        __labeled(file, 'Left Surface at', dt.strftime(ts_format))
        at = dive.reach_surface_time
        __labeled(file, 'Returned to Surface at', at.strftime(ts_format))
        ui = at - dt
        __labeled(file, 'Underwater Interval', 
                  '%s minutes' % int(ui.seconds / 60))
        __labeled(file, 'Max Depth', '%s %s' % (dive.max_depth, log.depth_unit))
        __labeled(file, 'Min Water Temperature', 
                  '%s %s' % (dive.min_water_temperature, log.temperature_unit))
        __labeled(file, 'Recording Interval', 
                  divelog.format_recording_interval(dive.recording_interval))
        __close(file, 'div')

        __open(file, 'div', 'container')
        __topen(file, ['Elapsed Time', 'Depth', 'Water Temperature', 'Ascent Rate'],
                classes='table table-striped table-condensed')
        for detail in dive.record:
            if detail.ascent_rate_violation:
                arv = '<span class="warning">ARV</span>'
            else:
                arv = ''
            if detail.decompression_violation:
                dv = '<span class="warning">DV</span>'
            else:
                dv = ''
            __trow(file, [
                    str(detail.elapsed_time),
                    '%s %s' % (detail.depth, log.depth_unit),
                    '%s %s' %
                       (detail.water_temperature, log.temperature_unit),
                    '%s %s %s' % (detail.ascent_rate, arv, dv)])
        __tclose(file)
        __close(file, 'div')

    __close(file, 'body')
    __close(file, 'hmtl')
