import rclpy
from rclpy.node import Node

#from std_msgs.msg import String
from nav_msgs.msg import Odometry


class OdomSubscriber(Node):

    def __init__(self):
        super().__init__('odom_subscriber')
        self.subscription = self.create_subscription( # Tipo mensaje, topic, rutina, QoS 
            Odometry,
            '/wheel/odometry',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.twist.twist.linear) # Imprimir


def main(args=None):
    rclpy.init(args=args)

    odom_subscriber = OdomSubscriber()

    rclpy.spin(odom_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    odom_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()