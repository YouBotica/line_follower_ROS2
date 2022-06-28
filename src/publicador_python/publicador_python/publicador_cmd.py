# Float32, string, bool, Float32MultiArray
# geometry_msgs/msg/Twist

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

class PublicadorCMD(Node):

    def __init__(self):
        super().__init__('publicador_cmd')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10) #(tipo_mensaje, nombre_topic, QoS)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.1
        #msg.angular.z
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)


def main(args=None):
    rclpy.init(args=args)

    publicador_cmd = PublicadorCMD()

    rclpy.spin(publicador_cmd)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    publicador_cmd.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()