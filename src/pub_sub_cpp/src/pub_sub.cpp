#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp" // Libreria que ros2 maneja de C++
#include "geometry_msgs/msg/twist.hpp" //Tipo de mensaje que vamos a publicar
#include "nav_msgs/msg/odometry.hpp" //Este es el tipo de mensaje al que nos vamos subscribir


using namespace std::chrono_literals;
using std::placeholders::_1;

/* This example creates a subclass of Node and uses std::bind() to register a
* member function as a callback from the timer. */

class PublicadorMovimiento : public rclcpp::Node
{
  public:
    PublicadorMovimiento()
    : Node("publicador_movimiento")
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10); // Nodo publicador, declaracion
        timer_ = this->create_wall_timer(
        100ms, std::bind(&PublicadorMovimiento::timer_callback, this));

        subscription_ = this->create_subscription<nav_msgs::msg::Odometry>("/wheel/odometry", 10, std::bind(&PublicadorMovimiento::subscriptor_callback, this, _1));
    }

  private:
    void timer_callback()
    {
      auto message = geometry_msgs::msg::Twist();
      message.linear.x = 0.05; // 0.05 m/seg hacia adelante
      //RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.linear.x.c_str());
      publisher_->publish(message);
    }

    void subscriptor_callback(const nav_msgs::msg::Odometry::SharedPtr msg) const
    {
      RCLCPP_INFO(this->get_logger(), "I heard: '%f'", msg->twist.twist.linear.x);
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PublicadorMovimiento>());
  rclcpp::shutdown();
  return 0;
}
