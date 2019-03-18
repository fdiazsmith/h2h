import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;
JSONObject settings;

fHR fhr;

// GLOBALS variables
int PORT;
String IP;
String ADDRESS;

/**
* - useful to always have in a Pricessing day/
* @method settings
*/
void settings( ){

  settings = loadJSONObject("settings.json");

  JSONObject size;
  size = settings.getJSONObject("size");
  IP = settings.getString("IP");
  PORT = settings.getInt("port");
  ADDRESS = settings.getString("address");
  size(size.getInt("width"), size.getInt("height"));

  // here we could add a check to see if the widht and height ar defined
  // go go full screen if they are not.
  // fullScreen( );
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this,PORT);

  /* myRemoteLocation is a NetAddress. a NetAddress takes 2 parameters,
   * an ip address and a port number. myRemoteLocation is used as parameter in
   * oscP5.send() when sending osc packets to another computer, device,
   * application. usage see below. for testing purposes the listening port
   * and the port of the remote location address are the same, hence you will
   * send messages back to this sketch.
   */
  myRemoteLocation = new NetAddress(IP,PORT);
}
/**
*
* @method setup
*/
void setup() {
  size(600, 600);

  fhr = new fHR( );
  if (frame != null) {
    surface.setResizable(true);
  }
}
/**
*
* @method draw
*/
void draw( ) {

  fhr.update();
}
/**
*
* @method oscEvent
* @params theOscMessage
*/
void oscEvent(OscMessage theOscMessage) {
  String addrPattern = theOscMessage.addrPattern();

  // Analogue input values
  if (addrPattern.equals(ADDRESS)) {
    // println(theOscMessage.get(0).intValue() );
    fhr.setBPM(theOscMessage.get(0).intValue());  // fhr.analogInputs[i] = theOscMessage.get(i).floatValue();

  }
  else {
    // If it did not match print address.
    println("This does not mach the pattern ",addrPattern);

  }

}

/**
*
* @method keyReleased
*/
void keyReleased( ) {
  fhr.released(key);
}

/**
*
* @method keyPressed
*/
void keyPressed( ) {
  fhr.pressed(key);
}

/**
*
* @method mouseMoved
*/
void mouseMoved( ) {
  fhr.mouseMoved();
}
/**
*
* @method mousePressed
*/
void mousePressed() {
  fhr.mousePressed();
}

void sendOSC() {
  // /* create a new osc message object */
  // OscMessage myMessage = new OscMessage("/test");
  //
  // myMessage.add(123); /* add an int to the osc message */
  // myMessage.add(12.34); /* add a float to the osc message */
  // myMessage.add("some text"); /* add a string to the osc message */
  //
  // /* send the message */
  // oscP5.send(myMessage, myRemoteLocation);
}
