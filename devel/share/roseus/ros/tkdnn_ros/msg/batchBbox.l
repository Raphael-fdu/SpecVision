;; Auto-generated. Do not edit!


(when (boundp 'tkdnn_ros::batchBbox)
  (if (not (find-package "TKDNN_ROS"))
    (make-package "TKDNN_ROS"))
  (shadow 'batchBbox (find-package "TKDNN_ROS")))
(unless (find-package "TKDNN_ROS::BATCHBBOX")
  (make-package "TKDNN_ROS::BATCHBBOX"))

(in-package "ROS")
;;//! \htmlinclude batchBbox.msg.html
(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))


(defclass tkdnn_ros::batchBbox
  :super ros::object
  :slots (_img_processed _batchBbox _latency ))

(defmethod tkdnn_ros::batchBbox
  (:init
   (&key
    ((:img_processed __img_processed) (instance sensor_msgs::Image :init))
    ((:batchBbox __batchBbox) (let (r) (dotimes (i 0) (push (instance tkdnn_ros::bbox :init) r)) r))
    ((:latency __latency) 0)
    )
   (send-super :init)
   (setq _img_processed __img_processed)
   (setq _batchBbox __batchBbox)
   (setq _latency (round __latency))
   self)
  (:img_processed
   (&rest __img_processed)
   (if (keywordp (car __img_processed))
       (send* _img_processed __img_processed)
     (progn
       (if __img_processed (setq _img_processed (car __img_processed)))
       _img_processed)))
  (:batchBbox
   (&rest __batchBbox)
   (if (keywordp (car __batchBbox))
       (send* _batchBbox __batchBbox)
     (progn
       (if __batchBbox (setq _batchBbox (car __batchBbox)))
       _batchBbox)))
  (:latency
   (&optional __latency)
   (if __latency (setq _latency __latency)) _latency)
  (:serialization-length
   ()
   (+
    ;; sensor_msgs/Image _img_processed
    (send _img_processed :serialization-length)
    ;; tkdnn_ros/bbox[] _batchBbox
    (apply #'+ (send-all _batchBbox :serialization-length)) 4
    ;; int32 _latency
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; sensor_msgs/Image _img_processed
       (send _img_processed :serialize s)
     ;; tkdnn_ros/bbox[] _batchBbox
     (write-long (length _batchBbox) s)
     (dolist (elem _batchBbox)
       (send elem :serialize s)
       )
     ;; int32 _latency
       (write-long _latency s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; sensor_msgs/Image _img_processed
     (send _img_processed :deserialize buf ptr-) (incf ptr- (send _img_processed :serialization-length))
   ;; tkdnn_ros/bbox[] _batchBbox
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _batchBbox (let (r) (dotimes (i n) (push (instance tkdnn_ros::bbox :init) r)) r))
     (dolist (elem- _batchBbox)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; int32 _latency
     (setq _latency (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get tkdnn_ros::batchBbox :md5sum-) "7652717954f28f2eeb1b5b5103c7ab8b")
(setf (get tkdnn_ros::batchBbox :datatype-) "tkdnn_ros/batchBbox")
(setf (get tkdnn_ros::batchBbox :definition-)
      "sensor_msgs/Image img_processed
bbox[] batchBbox
int32 latency
================================================================================
MSG: sensor_msgs/Image
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image
#

Header header        # Header timestamp should be acquisition time of image
                     # Header frame_id should be optical frame of camera
                     # origin of frame should be optical center of camera
                     # +x should point to the right in the image
                     # +y should point down in the image
                     # +z should point into to plane of the image
                     # If the frame_id here and the frame_id of the CameraInfo
                     # message associated with the image conflict
                     # the behavior is undefined

uint32 height         # image height, that is, number of rows
uint32 width          # image width, that is, number of columns

# The legal values for encoding are in file src/image_encodings.cpp
# If you want to standardize a new string format, join
# ros-users@lists.sourceforge.net and send an email proposing a new encoding.

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.h

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: tkdnn_ros/bbox
int32 x0
int32 x1
int32 y0
int32 y1
int32 cl
")



(provide :tkdnn_ros/batchBbox "7652717954f28f2eeb1b5b5103c7ab8b")


