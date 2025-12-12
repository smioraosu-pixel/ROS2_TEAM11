# [1] matplotlib. (n.d.). Infinite Lines#. Infinite lines - Matplotlib 3.10.7 documentation. https://matplotlib.org/stable/gallery/lines_bars_and_markers/axline.html#sphx-glr-gallery-lines-bars-and-markers-axline-py 
# [2] Stack overflow. (2016). Retrieved from https://stackoverflow.com/questions/35145555/python-real-time-plotting-ros-data
# [3] Oscilloscope#. Oscilloscope - Matplotlib 3.10.7 documentation. (n.d.). https://matplotlib.org/stable/gallery/animation/strip_chart.html 

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from sensor_msgs.msg import JointState
import matplotlib.pyplot as plt
import math


class Plotter(Node):
    def __init__(self):
        super().__init__('plotter')
        self.times = []                     # store time states are gotten
        self.joint_positions = []           # store joint angles
        
        # subscribes to joint state
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.js_callback,
            10
        )

        # Plot setup  [1][2]
        self.fig, self.ax = plt.subplots()

        plt.ion()
        plt.show() 
        self.ax.set_xlim(0, 10)               # x-axis limits
        self.ax.set_ylim(-math.pi, math.pi)   # y-axis limits

        self.line1, = self.ax.plot([], [], 'b', label='Joint 1')
        self.line2, = self.ax.plot([], [], 'g', label='Joint 2')
        self.line3, = self.ax.plot([], [], 'r', label='Joint 3')


    def js_callback(self, msg):
        print("callback called")
        current_time = self.get_clock().now()
        self.times.append(current_time.nanoseconds / 1e9) # Store timestamp
        self.joint_positions.append(list(msg.position))  # Store joint angles
        self.plotUpdate()
        # self.ax.set_xlim(max(0, self.times[-1]-10), self.times[-1]+0.1)  # [3] might be useful tbd
        self.ax.figure.canvas.draw()
        self.ax.legend()


    # Plotting
    def plotUpdate(self):
        lines = [self.line1, self.line2, self.line3]

        for i in range(3):
            jointPosition = [pos[i] for pos in self.joint_positions]
            lines[i].set_data(self.times, jointPosition)




        


def main(args=None):
    rclpy.init(args=args)
    
    plotter = Plotter()
    
    # make it so the node loops until we exit it
    try:
        rclpy.spin(plotter)
    except KeyboardInterrupt:
        pass
    
    plotter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()





