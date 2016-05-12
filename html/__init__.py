"""
This module implements a format handler that writes log data into
a very basis HTML format, useful for readable reports. There is not
a corresponding parser
"""
import divelog

FORMAT_NAME = 'HTML'

def parse(file):
    raise NotImplementedError()

def dump(log, file):
    """
    Serialize the log to the provided file object.
    """
    ts_format = '%A, %d. %B %Y %I:%M%p'

    file.write('<html><head></head><body>')
    file.write('<html>')
    file.write('</head>')
    file.write('<body>')

    file.write('<h1>Dive Log</h1>')

    if log.computer_model:
        file.write('<div class="dl.computer">')
        file.write('<div>')
        file.write('<label>Computer Model</label')
        file.write('<span>%s</span>' % log.computer_model)
        file.write('</div>')
        file.write('<div>')
        file.write('<label>Serial Number</label')
        file.write('<span>%s</span>' % log.computer_serial)
        file.write('</div>')
        file.write('</div>')

    file.write('<h2>Dives</h2>')
    for dive in log.dives:
        file.write('<h3>Dive Number %s</h3>' % dive.sequence_number)
        file.write('<div class="dl.dive">')
        file.write('<div>')
        file.write('<label>Left Surface at</label')
        dt = divelog.parse_timestamp(dive.leave_surface_time)
        file.write('<span>%s</span>' % dt.strftime(ts_format))
        file.write('</div>')
        file.write('<div>')
        file.write('<label>Returned to Surface at</label')
        at = divelog.parse_timestamp(dive.reach_surface_time)
        file.write('<span>%s</span>' % dt.strftime(ts_format))
        file.write('</div>')
        file.write('<div>')
        file.write('<label>Underwater interval</label')
        ui = at - dt
        file.write('<span>%s minutes</span>' % int(ui.seconds / 60))
        file.write('</div>')
        file.write('<div>')
        file.write('<label>Max Depth</label')
        file.write('<span>%s %s</span>' % (dive.max_depth, log.depth_unit))
        file.write('</div>')
        file.write('<div>')
        file.write('<label>Min Water Temperature</label')
        file.write('<span>%s %s</span>' % (dive.min_water_temperature, log.temperature_unit))
        file.write('</div>')
        file.write('<div>')
        file.write('<label>Recording Interval</label')
        file.write('<span>%s</span>' % divelog.format_recording_interval(dive.recording_interval))
        file.write('</div>')

        file.write('<div class="dl.divedetail">')
        file.write('<table>')
        file.write('<thead>')
        file.write('<tr>')
        file.write('<th>Elapsed time</th>')
        file.write('<th>Depth</th>')
        file.write('<th>Water Temperature</th>')
        file.write('<th>Ascent Rate</th>')
        file.write('</tr>')
        file.write('</thead>')
        file.write('<tbody>')
        for detail in dive.record:
            file.write('<tr>')
            file.write('<td>%s</td>' % detail.elapsed_time)
            file.write('<td>%s %s</td>' % (detail.depth, log.depth_unit))
            file.write('<td>%s %s</td>' % (detail.water_temperature, log.temperature_unit))
            if detail.ascent_rate_violation:
                arv = '<span class="dl.violation">ARV</span>'
            else:
                arv = ''
            if detail.decompression_violation:
                dv = '<span class="dl.violation">DV</span>'
            else:
                dv = ''
            file.write('<td>%s %s %s</td>' % (detail.ascent_rate, arv, dv))
            file.write('</tr>')
        file.write('</tbody>')
        file.write('</table>')
        file.write('</div>')

        file.write('</div>')
        
    file.write('</body>')
    file.write('</html>')
