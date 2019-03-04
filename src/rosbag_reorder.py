#!/usr/bin/python3
import rosbag
import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

with rosbag.Bag(out_file, 'w') as outbag:
    i = 1
    for topic, msg, t in rosbag.Bag(in_file).read_messages():
        # This also replaces tf timestamps under the assumption
        # that all transforms in the message share the same timestamp
        if topic == "/tf" and msg.transforms:
            outbag.write(topic, msg, msg.transforms[0].header.stamp)
        else:
            if (topic == "/point_map" and i % 20 == 0) or topic != "/point_map":
                if topic == "/point_map":
                    i = 1
                if msg._has_header:
                    outbag.write(topic, msg, msg.header.stamp if msg._has_header and msg.header.stamp.secs != 0 else t)
            else:
                i += 1
