//1 right 
//2 left
//direction right 4
//direction left 5


//code need an update (not final)

#define left   13
#define center 12
#define right  11
#define ENCB 2 //right
#define ENCA 3 //left
#define DIR_PIN4 4 //
#define DIR_PIN5 5
#define PWM_PIN9 9
#define PWM_PIN10  10

void readEncoderL();
void readEncoderR();
void setMotorL( float pwmVal);
void setMotorR( float pwmVal);

float kp_v = 3.7 ;
float ki_v = 30 * 3.7 ;

long    start_time= 0;
volatile int pulses_L = 0;
volatile int pulses_R = 0;
volatile double velocity_L = 0;
volatile double velocity_R = 0;
long        prevT = 0;

volatile double velocity_L2 = 0;
volatile double velocity_R2 = 0;
volatile double velocity_errorL = 0;
volatile double velocity_errorR = 0;



float  eintegral_L   =0;
float  eintegral_R   =0;

float Vel_ControlSignal_L = 0;
float Vel_ControlSignal_R = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(left, INPUT);
  pinMode(center, INPUT);
  pinMode(right, INPUT);
  
  pinMode(PWM_PIN9,OUTPUT);
  pinMode(DIR_PIN4,OUTPUT);
  pinMode(PWM_PIN10,OUTPUT);
  pinMode(DIR_PIN5,OUTPUT);

  pinMode(ENCA,INPUT_PULLUP);
  pinMode(ENCB,INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENCA),readEncoderL,RISING);
  attachInterrupt(digitalPinToInterrupt(ENCB),readEncoderR,RISING);


    analogWrite(PWM_PIN9,0);
    analogWrite(PWM_PIN10,0);

    digitalWrite(DIR_PIN4,HIGH);
    digitalWrite(DIR_PIN5,LOW);
    Serial.begin(9600);



}

void loop() {
  // put your main code here, to run repeatedly:
  bool leftV = digitalRead(left);
  bool centerV = digitalRead(center);
  bool rightV = digitalRead(right);
    Serial.print("left: ");
    Serial.print(leftV);
    Serial.print(" center: ");
    Serial.print(centerV);
    Serial.print(" right: ");
    Serial.println(rightV);
    
  if (leftV == 0  && rightV == 1) {
   velocity_L=0;
   velocity_R=10;
  } 
  else if (leftV == 1 && rightV == 0) {
   velocity_L=10;
   velocity_R=0;
  }
  else
  {
    velocity_L=10;
    velocity_R=10;
  }


  
  // time difference
  long currT = micros();
  double deltaT = ((double) (currT - prevT))/( 1.0e6 );
  prevT = currT;
  /* Read  position and velocity*/
  /*interrupt sandwich*/
  noInterrupts(); 
  velocity_L2=  (double)(((double)pulses_L / 19.894)      / (double)deltaT)  ;//(current pos. - last pos.) / time
  velocity_R2=  (double)(((double)pulses_R / 19.894)      / (double)deltaT ) ;//(current pos. - last pos.) / time
  pulses_L=0;
  pulses_R=0;
  interrupts();


   Serial.print(velocity_L2);
   Serial.print("  ");
   Serial.println(velocity_R2);

  velocity_errorL = velocity_L  -  velocity_L2;
  velocity_errorR = velocity_R  -  velocity_R2;

  eintegral_L = eintegral_L + velocity_errorL * deltaT;
  eintegral_R = eintegral_R + velocity_errorR * deltaT;

  Vel_ControlSignal_L =  kp_v  *  velocity_errorL + ki_v * eintegral_L;
  Vel_ControlSignal_R =  kp_v  *  velocity_errorR + ki_v * eintegral_R;

  float pwm_L = fabs(Vel_ControlSignal_L);
   if( pwm_L >= 255 )
   {
     pwm_L = 255;
     eintegral_L-= velocity_errorL * deltaT; //antiWindup
   }

   float pwm_R = fabs(Vel_ControlSignal_R);
   if( pwm_R>= 255 )
   {
     pwm_R = 255;
     eintegral_R-= velocity_errorR * deltaT; //antiWindup
   }

    analogWrite(PWM_PIN9,pwm_L);
    analogWrite(PWM_PIN10,pwm_R);

}



void readEncoderL()
{
  pulses_L++; 
}

void readEncoderR()
{
  pulses_R++;
}
