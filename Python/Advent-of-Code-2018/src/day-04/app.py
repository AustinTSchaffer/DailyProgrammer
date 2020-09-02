import os
import re
from collections import defaultdict
from datetime import datetime

class Event(object):
    def __init__(self, log_text):
        # [1518-09-17 23:48] Guard #1307 begins shift
        # [1518-09-17 23:48] falls asleep
        # [1518-09-17 23:48] wakes up

        self.raw_log = log_text

        match = re.match(r'\[(.+)\] (.+)', self.raw_log)

        self.datetime = datetime.strptime(match[1], r'%Y-%m-%d %H:%M')
        self.text = match[2]
        
        clean_text = self.text.strip().lower()
        guard_info = re.match(r'.*#(\d+).*', clean_text)

        self.guard_id = int(guard_info[1]) if guard_info else False
        self.asleep = clean_text == 'falls asleep'
        self.awake = clean_text == 'wakes up'

class GuardShift(object):
    def __init__(self, guard_id, shift_events):
        self.guard_id = guard_id
        self.shift_events = shift_events
        self.minutes_asleep = set()
        asleep_events = list(filter(lambda sh: sh.asleep, shift_events))
        awake_events = list(filter(lambda sh: sh.awake, shift_events))
        assert len(asleep_events) == len(awake_events)
        for asleep_event, awake_event in zip(asleep_events, awake_events):
            for minute in range(asleep_event.datetime.minute, awake_event.datetime.minute):
                self.minutes_asleep.add(minute)

class Guard(object):
    def __init__(self, guard_id, shifts):
        self.id = guard_id
        self.shifts = shifts

    def total_minutes_asleep(self):
        return sum(map(
            lambda shift: len(shift.minutes_asleep),
            self.shifts
        ))
    
    def minute_asleep_frequency(self):
        """
        Creates a histogram of the minutes between midnight and 1am,
        tracking the number of times that the guard was asleep for each
        minute. `{25: 4}` means that the guard was asleep at 12:25 on 4
        separate occasions.
        """
        minutes_asleep = defaultdict(int)
        for shift in self.shifts:
            for minute in shift.minutes_asleep:
                minutes_asleep[minute] += 1
        return minutes_asleep

    def highest_frequency_minute_asleep(self):
        """
        Returns (minute_asleep_the_most, frequency)
        """
        _max = (0, 0)
        for _cur in self.minute_asleep_frequency().items():
            if _cur[1] > _max[1]:
                _max = _cur
        return _max

CURRENT_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(CURRENT_DIR, 'data.txt')

def load_event_data(log_file):
    events = []
    with open(log_file, 'r') as data:
        for event in data:
            event = event.strip()
            if (event):
                events.append(Event(event))
    events.sort(key=lambda event: event.datetime)
    return events

def generate_guard_shifts(event_data):
    guard_shifts = []
    current_guard_id = None
    events_for_current_shift = []
    for event in event_data:
        if event.guard_id:
            if current_guard_id:
                guard_shifts.append(GuardShift(
                    current_guard_id,
                    events_for_current_shift,
                ))
                events_for_current_shift = []
            current_guard_id = event.guard_id
        else:
            events_for_current_shift.append(event)
    return guard_shifts

def create_guard_records(guard_shifts):
    guards = {}
    for shift in guard_shifts:
        guard_id = shift.guard_id
        if guard_id not in guards:
            guards[guard_id] = Guard(guard_id, [])
        guards[guard_id].shifts.append(shift)
    return [guard for _,guard in guards.items()]

def part1(guards):
    sleepiest_guards_first = sorted(
        guards,
        key=lambda g: g.total_minutes_asleep(),
        reverse = True
    )
    print('Sleepiest Guard:', sleepiest_guards_first[0].id)
    print('Minutes Asleep:', sleepiest_guards_first[0].total_minutes_asleep())
    print('guard id * minute asleep the most:', sleepiest_guards_first[0].id * sleepiest_guards_first[0].highest_frequency_minute_asleep()[0])
    print('Done')

def part2(guards):
    are_these_guys_even_working = sorted(
        guards,
        key=lambda guard: guard.highest_frequency_minute_asleep()[1],
        reverse=True
    )
    sleepiest_guards_first = are_these_guys_even_working
    print('Most Consistently Sleepy Guard:', sleepiest_guards_first[0].id)
    print('Minutes Asleep:', sleepiest_guards_first[0].total_minutes_asleep())
    print('guard id * minute asleep the most:', sleepiest_guards_first[0].id * sleepiest_guards_first[0].highest_frequency_minute_asleep()[0])
    print('Done')

if __name__ == "__main__":
    events = load_event_data(LOG_FILE)
    guard_shifts = generate_guard_shifts(events)
    guards = create_guard_records(guard_shifts)
    part1(guards)
    part2(guards) 

