#!/usr/bin/env python
import rospy
import rosgraph
import time
import sys
# packageName.FolderName
from unity_robotics_msgs.msg import Pos


TOPIC_NAME = 'pos'
NODE_NAME = 'position_publisher'


def post_string(myargv):
    # Init publisher object
    pub = rospy.Publisher(TOPIC_NAME, Pos, queue_size=10)
    # Init unique node
    rospy.init_node(NODE_NAME, anonymous=True)
    
    r = rospy.Rate(60) #10hz
    print("Robot id: ")
    id = int(input())    
    # Init as ROS String
    msg = Pos()
    # Set data
    msg.id = id

    mult = 0.01
    mult_x = mult
    mult_y = mult
    mult_z = mult

    pos_x = 2
    pos_y = 1
    pos_z = 2

    max_x = 3
    min_x = 1
    max_y = 2.3
    min_y = 1
    max_z = 2
    min_z = 1

    while not rospy.is_shutdown():
        if pos_x > max_x:
            mult_x = (-1) * mult
        elif pos_x < min_x:
            mult_x = mult
        pos_x += mult_x
           
        if pos_y > max_y:
            mult_y = (-1) * mult
        elif pos_y < min_y:
           mult_y = mult
        pos_y += mult_y
           
        if pos_z > max_z:
            mult_z = (-1) * mult
        elif pos_z < min_z:
           mult_z = mult
        pos_z += mult_z

        msg.x = pos_x
        msg.y = pos_y
        msg.z = pos_z

        #wait_for_connections(pub, TOPIC_NAME)
        pub.publish(msg)
        r.sleep()

    


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
