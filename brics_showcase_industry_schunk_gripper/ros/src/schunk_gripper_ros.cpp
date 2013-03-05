// ROS includes
#include <ros/ros.h>
#include <dynamic_reconfigure/server.h>
#include <brics_showcase_industry_schunk_gripper/schunk_gripperConfig.h>

// ROS message includes
#include <brics_showcase_industry_interfaces/MoveGripper.h>




#include <schunk_gripper_common.cpp>


class schunk_gripper_ros
{
	public:
		ros::NodeHandle n_;
		
		dynamic_reconfigure::Server<brics_showcase_industry_schunk_gripper::schunk_gripperConfig> server;
  		dynamic_reconfigure::Server<brics_showcase_industry_schunk_gripper::schunk_gripperConfig>::CallbackType f;
		

		

	ros::ServiceServer MoveGripper_;
        
 
        schunk_gripper_data component_data_;
        schunk_gripper_config component_config_;
        schunk_gripper_impl component_implementation_;

        schunk_gripper_ros()
        {
       	
  			f = boost::bind(&schunk_gripper_ros::configure_callback, this, _1, _2);
  			server.setCallback(f);
        	
        	
        		std::string MoveGripper_remap;
        		n_.param("MoveGripper_remap", MoveGripper_remap, (std::string)"MoveGripper");
        		MoveGripper_ = n_.advertiseService<brics_showcase_industry_interfaces::MoveGripper::Request , brics_showcase_industry_interfaces::MoveGripper::Response>(MoveGripper_remap, boost::bind(&schunk_gripper_impl::callback_MoveGripper, &component_implementation_,_1,_2,component_config_));
        
  	

				n_.param("dev_string", component_config_.dev_string, (std::string)"/dev/pcan32");
				n_.param("open_pos", component_config_.open_pos, (double)1.0);
				n_.param("close_pos", component_config_.close_pos, (double)1.0);
				n_.param("baudrate", component_config_.baudrate, (int)1000);
				n_.param("modul_id", component_config_.modul_id, (int)12);
				n_.param("speed", component_config_.speed, (double)0.01);
            
        }
		
        
		
		void configure_callback(brics_showcase_industry_schunk_gripper::schunk_gripperConfig &config, uint32_t level) 
		{
				component_config_.dev_string = config.dev_string;
				component_config_.open_pos = config.open_pos;
				component_config_.close_pos = config.close_pos;
				component_config_.baudrate = config.baudrate;
				component_config_.modul_id = config.modul_id;
				component_config_.speed = config.speed;
		}

        void configure()
        {
			component_implementation_.configure(component_config_);
        }

        void update()
        {
            component_implementation_.update(component_data_, component_config_);
    
        }
 
};

int main(int argc, char** argv)
{

	ros::init(argc, argv, "schunk_gripper");

	schunk_gripper_ros node;
    node.configure();

 // if cycle time == 0 do a spin() here without calling node.update() 
	ros::spin();
	
    return 0;
}
