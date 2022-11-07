#! /usr/bin/env python3

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
import time
from multiprocessing import Queue
import threading

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = Queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except Queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

rospy.init_node('camera_processing_right')
bridge = CvBridge()
#pub_image = rospy.Publisher('/usb_cam/compressed/image_left', CompressedImage, tcp_nodelay=True, queue_size=1)
pub_image2 = rospy.Publisher('/usb_cam/compressed/image_right', CompressedImage, tcp_nodelay=True, queue_size=1)
#cam1 = cv2.VideoCapture(2, cv2.CAP_V4L)
#cam1.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
#cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
#cam1.set(cv2.CAP_PROP_FPS, 30)
#cam1.set(cv2.CAP_PROP_BUFFERSIZE, 2)
cam2 = cv2.VideoCapture(4, cv2.CAP_V4L)
cam2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cam2.set(cv2.CAP_PROP_FPS, 30)
cam2.set(cv2.CAP_PROP_BUFFERSIZE, 2)

#cap = VideoCapture(0)
while not rospy.is_shutdown():
    start = time.time()
    ##ret1, frame1 = cam1.read()
    ##frame1 = bridge.cv2_to_compressed_imgmsg(frame1)
    ##pub_image.publish(frame1)
    ret2, frame2 = cam2.read()
    frame2 = bridge.cv2_to_compressed_imgmsg(frame2)
    pub_image2.publish(frame2)
    #time.sleep(0.03)
    fps = round(1 / (time.time() - start), 1)
    print('FPS:', fps)

