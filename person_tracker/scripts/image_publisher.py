import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    rospy.init_node('camera_image_publisher', anonymous=True)
    image_pub = rospy.Publisher('/camera_topic', Image, queue_size=10)
    bridge = CvBridge()

    cap = cv2.VideoCapture(0)

    while not rospy.is_shutdown():
        ret, frame = cap.read()

        if not ret:
            break

        # OpenCV画像をROS画像メッセージに変換
        ros_image_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

        # 画像メッセージをパブリッシュ
        image_pub.publish(ros_image_msg)

    cap.release()

if __name__ == '__main__':
    main()

