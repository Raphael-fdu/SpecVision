// Generated by gencpp from file tkdnn_ros/bbox.msg
// DO NOT EDIT!


#ifndef TKDNN_ROS_MESSAGE_BBOX_H
#define TKDNN_ROS_MESSAGE_BBOX_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace tkdnn_ros
{
template <class ContainerAllocator>
struct bbox_
{
  typedef bbox_<ContainerAllocator> Type;

  bbox_()
    : x0(0)
    , x1(0)
    , y0(0)
    , y1(0)
    , cl(0)  {
    }
  bbox_(const ContainerAllocator& _alloc)
    : x0(0)
    , x1(0)
    , y0(0)
    , y1(0)
    , cl(0)  {
  (void)_alloc;
    }



   typedef int32_t _x0_type;
  _x0_type x0;

   typedef int32_t _x1_type;
  _x1_type x1;

   typedef int32_t _y0_type;
  _y0_type y0;

   typedef int32_t _y1_type;
  _y1_type y1;

   typedef int32_t _cl_type;
  _cl_type cl;





  typedef boost::shared_ptr< ::tkdnn_ros::bbox_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::tkdnn_ros::bbox_<ContainerAllocator> const> ConstPtr;

}; // struct bbox_

typedef ::tkdnn_ros::bbox_<std::allocator<void> > bbox;

typedef boost::shared_ptr< ::tkdnn_ros::bbox > bboxPtr;
typedef boost::shared_ptr< ::tkdnn_ros::bbox const> bboxConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::tkdnn_ros::bbox_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::tkdnn_ros::bbox_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::tkdnn_ros::bbox_<ContainerAllocator1> & lhs, const ::tkdnn_ros::bbox_<ContainerAllocator2> & rhs)
{
  return lhs.x0 == rhs.x0 &&
    lhs.x1 == rhs.x1 &&
    lhs.y0 == rhs.y0 &&
    lhs.y1 == rhs.y1 &&
    lhs.cl == rhs.cl;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::tkdnn_ros::bbox_<ContainerAllocator1> & lhs, const ::tkdnn_ros::bbox_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace tkdnn_ros

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::tkdnn_ros::bbox_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::tkdnn_ros::bbox_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::tkdnn_ros::bbox_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::tkdnn_ros::bbox_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::tkdnn_ros::bbox_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::tkdnn_ros::bbox_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::tkdnn_ros::bbox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "78c33cb31c7f77f91beaa53c3f855838";
  }

  static const char* value(const ::tkdnn_ros::bbox_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x78c33cb31c7f77f9ULL;
  static const uint64_t static_value2 = 0x1beaa53c3f855838ULL;
};

template<class ContainerAllocator>
struct DataType< ::tkdnn_ros::bbox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "tkdnn_ros/bbox";
  }

  static const char* value(const ::tkdnn_ros::bbox_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::tkdnn_ros::bbox_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int32 x0\n"
"int32 x1\n"
"int32 y0\n"
"int32 y1\n"
"int32 cl\n"
;
  }

  static const char* value(const ::tkdnn_ros::bbox_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::tkdnn_ros::bbox_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.x0);
      stream.next(m.x1);
      stream.next(m.y0);
      stream.next(m.y1);
      stream.next(m.cl);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct bbox_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::tkdnn_ros::bbox_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::tkdnn_ros::bbox_<ContainerAllocator>& v)
  {
    s << indent << "x0: ";
    Printer<int32_t>::stream(s, indent + "  ", v.x0);
    s << indent << "x1: ";
    Printer<int32_t>::stream(s, indent + "  ", v.x1);
    s << indent << "y0: ";
    Printer<int32_t>::stream(s, indent + "  ", v.y0);
    s << indent << "y1: ";
    Printer<int32_t>::stream(s, indent + "  ", v.y1);
    s << indent << "cl: ";
    Printer<int32_t>::stream(s, indent + "  ", v.cl);
  }
};

} // namespace message_operations
} // namespace ros

#endif // TKDNN_ROS_MESSAGE_BBOX_H
