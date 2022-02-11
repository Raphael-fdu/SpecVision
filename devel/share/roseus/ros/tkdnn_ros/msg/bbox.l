;; Auto-generated. Do not edit!


(when (boundp 'tkdnn_ros::bbox)
  (if (not (find-package "TKDNN_ROS"))
    (make-package "TKDNN_ROS"))
  (shadow 'bbox (find-package "TKDNN_ROS")))
(unless (find-package "TKDNN_ROS::BBOX")
  (make-package "TKDNN_ROS::BBOX"))

(in-package "ROS")
;;//! \htmlinclude bbox.msg.html


(defclass tkdnn_ros::bbox
  :super ros::object
  :slots (_x0 _x1 _y0 _y1 _cl ))

(defmethod tkdnn_ros::bbox
  (:init
   (&key
    ((:x0 __x0) 0)
    ((:x1 __x1) 0)
    ((:y0 __y0) 0)
    ((:y1 __y1) 0)
    ((:cl __cl) 0)
    )
   (send-super :init)
   (setq _x0 (round __x0))
   (setq _x1 (round __x1))
   (setq _y0 (round __y0))
   (setq _y1 (round __y1))
   (setq _cl (round __cl))
   self)
  (:x0
   (&optional __x0)
   (if __x0 (setq _x0 __x0)) _x0)
  (:x1
   (&optional __x1)
   (if __x1 (setq _x1 __x1)) _x1)
  (:y0
   (&optional __y0)
   (if __y0 (setq _y0 __y0)) _y0)
  (:y1
   (&optional __y1)
   (if __y1 (setq _y1 __y1)) _y1)
  (:cl
   (&optional __cl)
   (if __cl (setq _cl __cl)) _cl)
  (:serialization-length
   ()
   (+
    ;; int32 _x0
    4
    ;; int32 _x1
    4
    ;; int32 _y0
    4
    ;; int32 _y1
    4
    ;; int32 _cl
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _x0
       (write-long _x0 s)
     ;; int32 _x1
       (write-long _x1 s)
     ;; int32 _y0
       (write-long _y0 s)
     ;; int32 _y1
       (write-long _y1 s)
     ;; int32 _cl
       (write-long _cl s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _x0
     (setq _x0 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _x1
     (setq _x1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _y0
     (setq _y0 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _y1
     (setq _y1 (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _cl
     (setq _cl (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get tkdnn_ros::bbox :md5sum-) "78c33cb31c7f77f91beaa53c3f855838")
(setf (get tkdnn_ros::bbox :datatype-) "tkdnn_ros/bbox")
(setf (get tkdnn_ros::bbox :definition-)
      "int32 x0
int32 x1
int32 y0
int32 y1
int32 cl
")



(provide :tkdnn_ros/bbox "78c33cb31c7f77f91beaa53c3f855838")


