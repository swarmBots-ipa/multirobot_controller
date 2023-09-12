import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.executors import SingleThreadedExecutor
from rclpy.executors import ExternalShutdownException

class VelocityController(Node):
    def __init__(self):
        super().__init__('velocity_controller')
        self.agents = ['/agent_0', '/agent_1', '/agent_2', '/agent_3']  # Add more agents as needed
        self.publisher_list = []

        for agent in self.agents:
            topic = agent + '/cmd_vel'
            self.publisher_list.append(self.create_publisher(Twist, topic, 10))
        self.width = 1.0
        self.length = 1.0
        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
    def cmd_vel_callback(self, msg):
        # Publish the received velocity command to each agent's cmd_vel topic
        for publisher in self.publisher_list:
            publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    controller = VelocityController()

    executor = SingleThreadedExecutor()
    executor.add_node(controller)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        executor.shutdown()
        rclpy.try_shutdown()

if __name__ == '__main__':
    main()
