; Auto-generated. Do not edit!


(cl:in-package tkdnn_ros-msg)


;//! \htmlinclude bbox.msg.html

(cl:defclass <bbox> (roslisp-msg-protocol:ros-message)
  ((x0
    :reader x0
    :initarg :x0
    :type cl:integer
    :initform 0)
   (x1
    :reader x1
    :initarg :x1
    :type cl:integer
    :initform 0)
   (y0
    :reader y0
    :initarg :y0
    :type cl:integer
    :initform 0)
   (y1
    :reader y1
    :initarg :y1
    :type cl:integer
    :initform 0)
   (cl
    :reader cl
    :initarg :cl
    :type cl:integer
    :initform 0))
)

(cl:defclass bbox (<bbox>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <bbox>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'bbox)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tkdnn_ros-msg:<bbox> is deprecated: use tkdnn_ros-msg:bbox instead.")))

(cl:ensure-generic-function 'x0-val :lambda-list '(m))
(cl:defmethod x0-val ((m <bbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:x0-val is deprecated.  Use tkdnn_ros-msg:x0 instead.")
  (x0 m))

(cl:ensure-generic-function 'x1-val :lambda-list '(m))
(cl:defmethod x1-val ((m <bbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:x1-val is deprecated.  Use tkdnn_ros-msg:x1 instead.")
  (x1 m))

(cl:ensure-generic-function 'y0-val :lambda-list '(m))
(cl:defmethod y0-val ((m <bbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:y0-val is deprecated.  Use tkdnn_ros-msg:y0 instead.")
  (y0 m))

(cl:ensure-generic-function 'y1-val :lambda-list '(m))
(cl:defmethod y1-val ((m <bbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:y1-val is deprecated.  Use tkdnn_ros-msg:y1 instead.")
  (y1 m))

(cl:ensure-generic-function 'cl-val :lambda-list '(m))
(cl:defmethod cl-val ((m <bbox>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tkdnn_ros-msg:cl-val is deprecated.  Use tkdnn_ros-msg:cl instead.")
  (cl m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <bbox>) ostream)
  "Serializes a message object of type '<bbox>"
  (cl:let* ((signed (cl:slot-value msg 'x0)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'x1)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'y0)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'y1)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'cl)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <bbox>) istream)
  "Deserializes a message object of type '<bbox>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'x0) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'x1) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'y0) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'y1) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'cl) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<bbox>)))
  "Returns string type for a message object of type '<bbox>"
  "tkdnn_ros/bbox")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'bbox)))
  "Returns string type for a message object of type 'bbox"
  "tkdnn_ros/bbox")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<bbox>)))
  "Returns md5sum for a message object of type '<bbox>"
  "78c33cb31c7f77f91beaa53c3f855838")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'bbox)))
  "Returns md5sum for a message object of type 'bbox"
  "78c33cb31c7f77f91beaa53c3f855838")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<bbox>)))
  "Returns full string definition for message of type '<bbox>"
  (cl:format cl:nil "int32 x0~%int32 x1~%int32 y0~%int32 y1~%int32 cl~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'bbox)))
  "Returns full string definition for message of type 'bbox"
  (cl:format cl:nil "int32 x0~%int32 x1~%int32 y0~%int32 y1~%int32 cl~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <bbox>))
  (cl:+ 0
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <bbox>))
  "Converts a ROS message object to a list"
  (cl:list 'bbox
    (cl:cons ':x0 (x0 msg))
    (cl:cons ':x1 (x1 msg))
    (cl:cons ':y0 (y0 msg))
    (cl:cons ':y1 (y1 msg))
    (cl:cons ':cl (cl msg))
))
