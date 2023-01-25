#!/usr/bin/env python
import rospy
import rosgraph
import time
import sys
from std_msgs.msg import String


TOPIC_NAME = 'string'
NODE_NAME = 'string_publisher'


def post_string(myargv):
    # Init publisher object
    pub = rospy.Publisher(TOPIC_NAME, String, queue_size=10)
    # Init unique node
    rospy.init_node(NODE_NAME, anonymous=True)
    
    argString = ' '.join(myargv[1:])
    # Init as ROS String
    help_msg = String()
    # Set data
    help_msg.data = argString

    #wait_for_connections(pub, TOPIC_NAME)
    pub.publish(help_msg)

    time.sleep(0.1)


def wait_for_connections(pub, topic):
    ros_master = rosgraph.Master('/rostopic')
    topic = rosgraph.names.script_resolve_name('rostopic', topic)
    num_subs = 0
    for sub in ros_master.getSystemState()[1]:
        if sub[0] == topic:
            num_subs+=1

    for i in range(10):
        if pub.get_num_connections() == num_subs:
            return
        time.sleep(0.1)
    raise RuntimeError("failed to get publisher")


if __name__ == '__main__':
    try:
        myargv = rospy.myargv(argv=sys.argv)
        post_string(myargv)
    except rospy.ROSInterruptException:
        pass
