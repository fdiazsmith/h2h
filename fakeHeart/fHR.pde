/**
 * @class fHR
 *

  Y          R
  |         /|
  |    __  |  \  /\___
  |      \/    |/  O ->  me lo invente
  |      Q     S
  |______________________X

 */
class fHR {
  color backgroundColor = color(255);


  int bpm = 40;
  int MINUTE = 60000;
  float IBI = MINUTE/bpm;
  float fakeSignal = 0;

  float Ry = 0.95,
        Rx = 0.25,
        Sy = 0.95,
        Sx = 0.25,
        Oy = 0.47,
        Ox = 0.35;

  int xPos = 0;



  // private:
  private float ibi = MINUTE/bpm;
  private int lastBeat = 0;
  private int NORMAL = 1;
  private int previousYPos = 0;
  private int previousWidth = 0;
  private int previousHeigth = 0;

  private float noiseSpeed = 0.01,
                noiseWalker = 0;
  private float ibiNoiseSpeed = 0.2,
                ibiNoiseWalker = 0;

  private float Shp1 = 0.46000004,
                Shp2 = 1.6399996,
                Ohp1 = 0.02,
                Ohp2 = 1.0299994;
  /**
   * @contructor
   */
  fHR( ) {

  }


  /**
   * @method set
   * @param {int} _bpm
   * sets the inter beat interval, based on current beats per minute received
   */
  void setBPM( int _bpm) {
    bpm = _bpm;
    ibi = MINUTE/bpm;
  }

  /**
   * @method getIBI
   *  add a little noise so that the intervals are not as mechanical
   */
  float getIBI() {
    ibiNoiseWalker += ibiNoiseSpeed;
    return ibi + ( (ibi*0.6) * noise(ibiNoiseWalker) );
  }

  /**
   * @method update
   */
  void update( ) {
    // Trace analogue input values

    strokeWeight(1);  // trace width
    stroke(255);      // trace colour

    float s  = fakeSignal();
    // background(s*255, 20, 20);

    int yPos;
    stroke(255);
    yPos = (int) map(s , 0, 1, height, 0);

    line(xPos, previousYPos, xPos+1, yPos);
    previousYPos = yPos;

    // Restart if graph full or window resized
    if (++xPos >= width || previousWidth != width || previousHeigth != height) {
      previousWidth = width;
      previousHeigth = height;
      xPos = 0;
      drawBackground();
    }
  }
  /**
   * @method fakeSignal
   */
  float fakeSignal( ) {
    float sig =0;
    noiseWalker += noiseSpeed;

    float median = (float)NORMAL/2;
    int currentBeatTimer = millis() - lastBeat;
    if(  currentBeatTimer/(IBI*Sx) <=1 ){
     sig = bezierPoint(( median * Sy ), Shp1, Shp2, ( median * Sy )- .09, currentBeatTimer/(IBI*Sx));
     // sig = ( median * Sy )- .09;
    }
    else if(  ( currentBeatTimer - ( IBI*Sx ) ) / ( (IBI- (IBI*Sx) ) * Ox ) <=1 ){
      sig = bezierPoint(( median * Sy )- .09, Ohp1, Ohp2, ( median * Sy ) , ( currentBeatTimer - (IBI*Sx) ) /((IBI- (IBI*Sx) )*Ox)  );
    }
    else{
      sig = median + ( noise(noiseWalker) * .1);
    }

    if( currentBeatTimer > IBI ){
      lastBeat  = millis();
      IBI = getIBI();
      println(IBI);

    }

    return sig;
  }
  /**
   * @method drawBackground
   */
  void drawBackground() {
    strokeWeight(1);                          // rectangle border width
    PFont f = createFont("Arial", 16, true);  // Arial, 16 point, anti-aliasing on

    stroke(0);
    fill(0);
    rect(0, 0, width, height);

  }
  /**
   * @method released – handles keyReleased events
   * @param {char} _key
   */
  void released(char _key) {
    if ( _key == 's' ) {
      // code
    }
    else if(  _key == 'p'){

    }
  }
  /**
   * @method pressed – handles keyReleased events
   * @param {char} _key
   */
  void pressed(char _key) {
    if ( _key == 'w' ) {
      Ohp1 += 0.01;
    }
    else if(  _key == 's'){
      Ohp1 -= 0.01;
    }
    else if(  _key == 'o'){
      Ohp2 += 0.01;
    }
    else if(  _key == 'l'){
      Ohp2 -= 0.01;
    }
    println(Ohp1, Ohp2);
  }
  /**
   * @method mouseMoved
   */
  void mouseMoved() {
    // do something
  }
  /**
   * @method mousePressed
   */
  void mousePressed() {
    // do something
  }


  /**
   * @class modal – 
   */
  void modal( String message, float normal ) {
    float alpha = 1-(normal*normal);
    textAlign(CENTER, CENTER);
    fill(50, alpha*150);
    rect(0,0,width, height);
    fill(255, alpha*255);
    textSize(132);
    text(message, width/2, height/2);
  }
  /**
   * @class message – 
   */
  void message( String message, float x, float y ) {
    textAlign(LEFT, CENTER);
    fill(30, 180);
    textSize(16);
    text(message, (int)x, (int)y );
  }
}
