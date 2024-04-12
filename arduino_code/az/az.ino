
#include "AS5600.h"
#include <Servo.h>
#include "Arduino.h"

#define LASER_PIN 1

//Source for control system code : https://www.youtube.com/watch?v=RZW1PsfgVEI&t=317s
//Code for as5600 library : https://github.com/RobTillaart/AS5600

AS5600 as5600;   //  use default Wire
//sensor used in project

Servo twpro; 
//Servo motor

String data;
//Data from python script that controls setpoint for control system

double dt, lasttime ;
double integral , previous , output = 0;
double kp , ki , kd ;
//Variables for pid control system

double set_point = 0 ;
//Variabel that controls setpoint

int servo_input = 0;
//The output variable from the controller that is used to adjust the system and satisfy the reading from the sensor

float bias = 0;
//Since the sensor doesnt reset to zero properly, this bias is needed to adjust the bad zero position 

double error , sensor_value = 0;
double calibrated_sensor_value =0;
int servo_max_cw = 0;
int servo_max_ccw = 180;
int servo_zp = 90;
//Variables that control finer servo control since there is a massive deadzone

int servo_cw_dp =  87;
int servo_ccw_dp = 98 ;
// The value at which the servo doesnt move, so 87 and 98 , the servo moves
//
// 0                             87,88       90            97,98                         180
// I----------------CW-------------I----DZ---I------DZ-------I------------CCW-------------I
// 

int az = 0;
int theta = 0 ;
const int trigger_pin = 6;
int trigger_state ;



void setup()
{

  //////////////////////////// OVER HERE CONTROLS IF THE ARDUINO IS FOR AZ OR THETA////////////////////////////////////
  pinMode(trigger_pin, INPUT);
  pinMode(LED_BUILTIN, OUTPUT); 
  //////////////////////////// OVER HERE CONTROLS IF THE ARDUINO IS FOR AZ OR THETA////////////////////////////////////

  pinMode(LASER_PIN, OUTPUT);


  kp = 0.8;
  ki = 0.05;
  kd = 0.05;
  //Control system parameters initilazied

  twpro.attach(0);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
  //Serial.println(__FILE__);
  //Serial.print("AS5600_LIB_VERSION: ");
  //Serial.println(AS5600_LIB_VERSION);

  Wire.begin();

  as5600.begin(4);  //  set direction pin.
  as5600.setDirection(AS5600_COUNTERCLOCK_WISE);  //  

  //Serial.println(as5600.getAddress());

  //  as5600.setAddress(0x40);  //  AS5600L only

  //int b = as5600.isConnected();
  //Serial.print("Connect: ");
  //Serial.println(b);

  delay(1000);
}

void loop()
{               
  //////////////////////////// OVER HERE CONTROLS IF THE ARDUINO IS FOR AZ OR THETA////////////////////////////////////
  trigger_state = digitalRead(trigger_pin);
  if (trigger_state == HIGH) 
  {
    az = 1;
    theta = 0;
    digitalWrite(LED_BUILTIN, HIGH);
    //Serial.println("AZ");
  }
  else 
  {
    az = 0;
    theta = 1;
    digitalWrite(LED_BUILTIN, LOW);
    //Serial.println("THETA");
  }
  //////////////////////////// OVER HERE CONTROLS IF THE ARDUINO IS FOR AZ OR THETA////////////////////////////////////

  
  double now = millis();
  dt = (now - lasttime )/ 1000.0;
  lasttime = now ;
  //Time for control system

  //sensor_value = (as5600.rawAngle() * AS5600_RAW_TO_DEGREES);
  sensor_value = (as5600.getCumulativePosition() * AS5600_RAW_TO_DEGREES) ;
  calibrated_sensor_value = sensor_value -bias ;
  //We use cumulative position to prevent overlooping from 360 to 0 and causing infinite loop 
  // and then add bias to correct if calibrated properly

  error = set_point - calibrated_sensor_value ;
  //Feedback 
  
  output = pid(-error);
  //Output for controller
  //If the servo turns the wrong way, its cause the line above needs to be output = pid(-error);
  
  servo_input = rectify_for_servo(output);
  //Controller output needs to be modified to be suited to servo input

  //Serial.println("---------------------------------");
  //Serial.println("Sensor reading is");
  //Serial.println(sensor_value);
  //Serial.println("");
  //Serial.println("Calibrated Sensor reading is");
  //Serial.println(calibrated_sensor_value);
  //Serial.println("");
  //Serial.println("Set point value is");
  //Serial.println(set_point);
  //Serial.println("");
  //Serial.println("Error value is");
  //Serial.println(error);
  //Serial.println("");
  //Serial.println("Output value is");
  //Serial.println(output);
  //Serial.println("");
  //Serial.println(" Rectified Servo input is");
  //Serial.println(servo_input);
  //Serial.println("");

  twpro.write(servo_input); 
  
  if (Serial.available() > 0) 
  { // Check if data is available to read
    data = Serial.readStringUntil('\r'); // Read the incoming data

    // Process the data
    //Serial.print("Received data: ");
    Serial.println(data);

    if (data.startsWith("l"))
    {
      turn_on();
    }
    if (data.startsWith("n"))
    {
      turn_off();
    }

    if ((az and data.startsWith("a") )  or  (theta and data.startsWith("t")))
    {
      
      data.remove(0,1);
      //Serial.println(data);
      
      if ( data.startsWith("u") )
      {
        set_point = set_point + 45;
      }
      if ( data.startsWith("d") )
      {
        set_point = set_point - 45;
      }
      if ( data.startsWith("r") )
      {
        Serial.println("This position is now ZERO degrees");
        //as5600.resetCumulativePosition(0); <-For some reason this function doesnt actually reset to zero, but instead to -18.4.
        bias = sensor_value   ;
        set_point = 0 ;
      }


      if (data.startsWith("z"))
      {
        set_point = 0;
      }
      //This is needed since  teh if statements belkow prevents zero from being the setpoint

      if (data.toFloat() != 0)
      {
        set_point = data.toFloat() ;
      }

      if(data.startsWith("n"))
      {
        data.remove(0,1);
        if (data.toFloat() != 0)
        {
          
          bias = bias + ( set_point - data.toFloat()) ;

          set_point = data.toFloat() ;
        }
      }
    }
  }
}

  
double rectify_for_servo(double controller_output)
{
  controller_output = (controller_output/4) + servo_zp ;
  //Actually scaling the value from <-360 to 360> to <0 to 180>
  //See christmas tree diagram

  if ( abs(controller_output- servo_zp ) < 0.3  )
  {
    return 90 ;
  }
  //If the controller is only outputting a correction signal of 0.3 or less, then the controller will just accept the current sensor reading as the setpoint value

  if ( (controller_output) < servo_zp )
  {
    return (controller_output - abs(servo_zp - servo_cw_dp)  ) ;
  }
  //Negative since the  cw deadpoint(88) is lower than the zp

  if ( (controller_output) >  servo_zp )
  {
    return (controller_output + abs(servo_zp - servo_ccw_dp)) ;
  }
  //Positive since the ccw dp(97) is higher than the zp

}

double pid(double error)
{
  double proportional = error ;
  integral += error * dt ;
  double derivative = (error - previous) / dt;
  previous = error ;
  double output = (kp * proportional);
  //Only proportional control is used

  //double output = (kp * proportional)+( ki * integral)+( kd * derivative);
  
  return output ;
}

void turn_on()
{
  digitalWrite(LASER_PIN, HIGH);
  //turns on the laser
}

void turn_off()
{
  digitalWrite(LASER_PIN, LOW);
  //turns off the laser
}



