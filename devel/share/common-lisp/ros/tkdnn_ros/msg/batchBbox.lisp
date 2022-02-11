; Auto-generated. Do not edit!


(cl:in-package tkdnn_ros-msg)


;//! \htmlinclude batchBbox.msg.html

(cl:defclass <batchBbox> (roslisp-msg-protocol:ros-message)
  ((img_processed
    :reader img_processed
    :initarg :img_processed
    :type sensor_msgs-msg:Image
    :initform (cl:make-instance 'sensor_msgs-msg:Image))
   (batchBbox
    :reader batchBbox
    :initarg :batchBbox
    :type (cl:vector tkdnn_ros-msg:bbox)
   :initform (cl:make-array 0 :element-type 'tkdnn_ros-msg:bbox :initial-element (cl:make-instance 'tkdnn_ros-msg:bbox)))
   (latency
    :reader latency
    :initarg :latency
    :type cl:integer
    :initform 0))
)

(cl:defclass batchBbox (<batchBbox>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <batchBbox>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'batchBbox)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tkdnn_ros-msg:<batchBbox> is deprecated: use tkdnn_ros-msg:batchBbox instead.")))

(cl:ensure-generic-function 'img_processed-val :lambda-list '(m))
(cl:defmethod img_processed-val ((m <batchBbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:img_processed-val is deprecated.  Use tkdnn_ros-msg:img_processed instead.")
  (img_processed m))

(cl:ensure-generic-function 'batchBbox-val :lambda-list '(m))
(cl:defmethod batchBbox-val ((m <batchBbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:batchBbox-val is deprecated.  Use tkdnn_ros-msg:batchBbox instead.")
  (batchBbox m))

(cl:ensure-generic-function 'latency-val :lambda-list '(m))
(cl:defmethod latency-val ((m <batchBbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:latency-val is deprecated.  Use tkdnn_ros-msg:latency instead.")
  (latency m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <batchBbox>) ostream)
  "Serializes a message object of type '<batchBbox>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'img_processed) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'batchBbox))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'batchBbox))
  (cl:let* ((signed (cl:slot-value msg 'latency)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <batchBbox>) istream)
  "Deserializes a message object of type '<batchBbox>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'img_processed) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'batchBbox) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'batchBbox)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'tkdnn_ros-msg:bbox))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'latency) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<batchBbox>)))
  "Returns string type for a message object of type '<batchBbox>"
  "tkdnn_ros/batchBbox")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'batchBbox)))
  "Returns string type for a message object of type 'batchBbox"
  "tkdnn_ros/batchBbox")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<batchBbox>)))
  "Returns md5sum for a message object of type '<batchBbox>"
  "7652717954f28f2eeb1b5b5103c7ab8b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'batchBbox)))
  "Returns md5sum for a message object of type 'batchBbox"
  "7652717954f28f2eeb1b5b5103c7ab8b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<batchBbox>)))
  "Returns full string definition for message of type '<batchBbox>"
  (cl:format cl:nil "sensor_msgs/Image img_processed~%bbox[] batchBbox~%int32 latency~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: tkdnn_ros/bbox~%int32 x0~%int32 x1~%int32 y0~%int32 y1~%int32 cl~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'batchBbox)))
  "Returns full string definition for message of type 'batchBbox"
  (cl:format cl:nil "sensor_msgs/Image img_processed~%bbox[] batchBbox~%int32 latency~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: tkdnn_ros/bbox~%int32 x0~%int32 x1~%int32 y0~%int32 y1~%int32 cl~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <batchBbox>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'img_processed))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'batchBbox) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <batchBbox>))
  "Converts a ROS message object to a list"
  (cl:list 'batchBbox
    (cl:cons ':img_processed (img_processed msg))
    (cl:cons ':batchBbox (batchBbox msg))
    (cl:cons ':latency (latency msg))
))
