/* -----------------------------------------------------------------------------
 * Example .ino file for arduino, compiled with CmdMessenger.h and
 * CmdMessenger.cpp in the sketch directory. 
 *----------------------------------------------------------------------------*/
//Changed on 5/5/2018

#include "CmdMessenger.h"
#include <Servo.h>
//#include "Math.h"

#define LEFT_PIN 9
#define RIGHT_PIN 10
#define ELBOW_PIN 6
#define SHOULDER_PIN 5
#define DRUM_PIN 11
#define MAX_DRUM 45
#define MAX_DELTA 10

double prev_drum = 90;

/*SoftwareSerial LEFT(NOT_A_PIN, LEFT_PIN); // RX on no pin (unused), TX on pin 11 (to S1).
SyRenSimplified Left(LEFT); // Use SWSerial as the serial port.

SoftwareSerial RIGHT(NOT_A_PIN, RIGHT_PIN); // RX on no pin (unused), TX on pin 11 (to S1).
SyRenSimplified Right(RIGHT); // Use SWSerial as the serial port.

SoftwareSerial DRUM(NOT_A_PIN, DRUM_PIN); // RX on no pin (unused), TX on pin 11 (to S1).
SyRenSimplified Drum(DRUM); // Use SWSerial as the serial port.
*/

Servo Drum;
Servo Left;
Servo Right;
Servo Shoulder;
Servo Elbow;


/* Define available CmdMessenger commands */
enum {
    left,
    right,
    shoulder,
    elbow,
    drum
};

/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');

/* Create callback functions to deal with incoming messages */

/* callback */
void on_left(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Left.write(value);
    /* Send result back */ 
    //c.sendBinCmd(left,value);

}

void on_right(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Right.write(value);
    /* Send result back */ 
    //c.sendBinCmd(right,value);

}

void on_shoulder(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Shoulder.write(value);
    /* Send result back */ 
    //c.sendBinCmd(shoulder,value);

}

void on_elbow(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    Elbow.write(value);
    /* Send result back */ 
    //c.sendBinCmd(elbow,value);

}

void on_drum(void){
    /* Grab two integers */
    int value = c.readBinArg<int>();
    value = map(value, -1000,1000,0,180);
    /*int error = value - prev_drum;
    
    if(abs(error) > MAX_DELTA){
      if(value > 90) 
        value = prev_drum + MAX_DELTA;
      else if(value < 90)
        value = prev_drum - MAX_DELTA;
    }

    if(value > 90 + MAX_DRUM)
      value = 90 + MAX_DRUM;
    else if( value < (90 - MAX_DRUM))
      value = 90 - MAX_DRUM;
    Drum.write(value);
    prev_drum = value;*/
    /* Send result back */ 
    //c.sendBinCmd(drum,value);

    Drum.write(value);

}



/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) { 
    c.attach(left,on_left);
    c.attach(right,on_right);
    c.attach(shoulder,on_shoulder);
    c.attach(elbow,on_elbow);
    c.attach(drum,on_drum);
}

void setup() {
    Drum.attach(DRUM_PIN,1000,2000);
    Left.attach(LEFT_PIN,1000,2000);
    Right.attach(RIGHT_PIN,1000,2000);
    Elbow.attach(ELBOW_PIN,1000,2000);
    Shoulder.attach(SHOULDER_PIN,1000,2000);
    Serial.begin(BAUD_RATE);
    attach_callbacks();    
}

void loop() {
    c.feedinSerialData();
    delay(10);
}
