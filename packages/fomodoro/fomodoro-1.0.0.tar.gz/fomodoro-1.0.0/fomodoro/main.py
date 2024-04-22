import curses
from curses import wrapper
from time import sleep, strftime, gmtime
from json import load, dump

from fomodoro.utils import States, SECONDS_FORMAT, INFO_FILE
from fomodoro.stopwatch import Stopwatch
from fomodoro.timer import Timer


stopwatch_obj = Stopwatch()
timer_obj = Timer()

def main(stdscr):
    """"""
    with open(INFO_FILE, 'r', encoding='utf-8') as info_file:
        info = load(info_file)

    curses.resize_term(3, 11)
    time_window = curses.newwin(1, 6, 1, 3)

    if info["stopwatch_state"] == "Pause" or info["stopwatch_state"] == " ":
        stopwatch_obj.start()
        stopwatch_obj.elapsed_seconds = info["elapsed_seconds"]

        while stopwatch_obj.state is States.START:
            sleep(1.0)
            stopwatch_obj.elapsed_seconds += 1
            stopwatch_obj.seconds += 1
            struct_time_stopwatch = gmtime(float(stopwatch_obj.elapsed_seconds))
            stopwatch_formated_seconds = strftime(SECONDS_FORMAT, struct_time_stopwatch)

            time_window.nodelay(True)
            time_window.clear()
            time_window.addstr(stopwatch_formated_seconds[0:], curses.A_BOLD)
            time_window.refresh()
            try:
                stopwatch_character = time_window.getkey()
                if stopwatch_character == "p":
                    stopwatch_obj.pause()
                    info["stopwatch_state"] = 'Pause'
                    info["elapsed_seconds"] = info["elapsed_seconds"] + stopwatch_obj.seconds
                    with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                        dump(info, info_file, indent=2)
                elif stopwatch_character == "s":
                    stopwatch_obj.stop()
                    info["stopwatch_state"] = 'Stop'
                    info["elapsed_seconds"] = info["elapsed_seconds"] + stopwatch_obj.seconds
                    with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                        dump(info, info_file, indent=2)
            except curses.error:
                stopwatch_character = None
    elif info["stopwatch_state"] == "Stop":
        if info["timer_state"] == " ":
            amount_of_seconds_for_the_timer: float = round(info["elapsed_seconds"] / 5)
        else:
            amount_of_seconds_for_the_timer: float = info["leftover_break_time_in_seconds"]

        timer_obj.break_time_in_seconds = int(amount_of_seconds_for_the_timer)
        timer_obj.start()

        while timer_obj.state is States.START:
            sleep(1.0)
            if timer_obj.break_time_in_seconds > 0:
                timer_obj.break_time_in_seconds -= 1
            else:
                timer_obj.stop()
                info["timer_state"] = " "
                info["leftover_break_time_in_seconds"] = 0
                info["elapsed_seconds"] = 0
                info["stopwatch_state"] = " "
            
            struct_time_timer = gmtime(timer_obj.break_time_in_seconds)
            timer_formated_seconds = strftime(SECONDS_FORMAT, struct_time_timer)

            time_window.nodelay(True)
            time_window.clear()
            time_window.addstr(timer_formated_seconds[0:], curses.A_BOLD)
            time_window.refresh()
            try:
                timer_character = time_window.getkey()
                if timer_character == "p":
                    timer_obj.pause()
                    info["timer_state"] = "Pause"
                    info["leftover_break_time_in_seconds"] = timer_obj.break_time_in_seconds
                    with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                        dump(info, info_file, indent=2)
            except curses.error:
                timer_character = None
            
            with open(INFO_FILE, 'w', encoding='utf-8') as info_file:
                dump(info, info_file, indent=2)

fomodoro = wrapper(main)
