// Auto-generated. Do not edit!

// (in-package tkdnn_ros.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let bbox = require('./bbox.js');
let sensor_msgs = _finder('sensor_msgs');

//-----------------------------------------------------------

class batchBbox {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.img_processed = null;
      this.batchBbox = null;
      this.latency = null;
    }
    else {
      if (initObj.hasOwnProperty('img_processed')) {
        this.img_processed = initObj.img_processed
      }
      else {
        this.img_processed = new sensor_msgs.msg.Image();
      }
      if (initObj.hasOwnProperty('batchBbox')) {
        this.batchBbox = initObj.batchBbox
      }
      else {
        this.batchBbox = [];
      }
      if (initObj.hasOwnProperty('latency')) {
        this.latency = initObj.latency
      }
      else {
        this.latency = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type batchBbox
    // Serialize message field [img_processed]
    bufferOffset = sensor_msgs.msg.Image.serialize(obj.img_processed, buffer, bufferOffset);
    // Serialize message field [batchBbox]
    // Serialize the length for message field [batchBbox]
    bufferOffset = _serializer.uint32(obj.batchBbox.length, buffer, bufferOffset);
    obj.batchBbox.forEach((val) => {
      bufferOffset = bbox.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [latency]
    bufferOffset = _serializer.int32(obj.latency, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type batchBbox
    let len;
    let data = new batchBbox(null);
    // Deserialize message field [img_processed]
    data.img_processed = sensor_msgs.msg.Image.deserialize(buffer, bufferOffset);
    // Deserialize message field [batchBbox]
    // Deserialize array length for message field [batchBbox]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.batchBbox = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.batchBbox[i] = bbox.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [latency]
    data.latency = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += sensor_msgs.msg.Image.getMessageSize(object.img_processed);
    length += 20 * object.batchBbox.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tkdnn_ros/batchBbox';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7652717954f28f2eeb1b5b5103c7ab8b';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    sensor_msgs/Image img_processed
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new batchBbox(null);
    if (msg.img_processed !== undefined) {
      resolved.img_processed = sensor_msgs.msg.Image.Resolve(msg.img_processed)
    }
    else {
      resolved.img_processed = new sensor_msgs.msg.Image()
    }

    if (msg.batchBbox !== undefined) {
      resolved.batchBbox = new Array(msg.batchBbox.length);
      for (let i = 0; i < resolved.batchBbox.length; ++i) {
        resolved.batchBbox[i] = bbox.Resolve(msg.batchBbox[i]);
      }
    }
    else {
      resolved.batchBbox = []
    }

    if (msg.latency !== undefined) {
      resolved.latency = msg.latency;
    }
    else {
      resolved.latency = 0
    }

    return resolved;
    }
};

module.exports = batchBbox;
