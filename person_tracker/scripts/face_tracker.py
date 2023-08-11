import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 as cv

class FaceTrackingNode:
    def __init__(self):
        rospy.init_node('face_tracking_node', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/camera_topic', Image, self.image_callback)
        self.image_pub = rospy.Publisher('/camera_topic2', Image, queue_size=10)

        self.HAAR_FILE = "/home/brlab/mypro/Turtlebot-PJ/turtlebot_ws/src/person_tracker/data/haarcascade_frontalface_default.xml"
        self.cascade = cv.CascadeClassifier(self.HAAR_FILE)

        #self.robot_controller = YourRobotController()  # ロボットの制御インスタンスを作成

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        face = self.cascade.detectMultiScale(frame)

        for x, y, w, h in face:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            print(x, y)
            
            # 顔の位置に応じて速度指令を計算
            # 速度指令をロボットに送信

        cv.imshow('frame', frame)
        cv.waitKey(1)

        # OpenCV画像をROS画像メッセージに変換
        ros_image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")

        # 画像メッセージをパブリッシュ
        self.image_pub.publish(ros_image_msg)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = FaceTrackingNode()
    node.run()

