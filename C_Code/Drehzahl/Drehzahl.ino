

const int pin_in = A0;
const int BTN_Test = A1;

const int LED_S = A4;
const int LED_M = A5;


int defa = HIGH;
int state = defa; 
bool detect = true;
bool state1 = false;

int reading;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 100;
int lastButtonState = defa;
int buttonState = defa;

int flag1 = true;
int mode = 0;

unsigned long t1 = 0;
unsigned long t2 = 0;
unsigned long T = 0;
unsigned long f = 0;
char userInput;

int cou = 0;

void setup() {
  pinMode(pin_in, INPUT);
  digitalWrite(pin_in, HIGH);
  pinMode(BTN_Test, INPUT);
  digitalWrite(BTN_Test, HIGH);
  
  pinMode(LED_S, OUTPUT);
  digitalWrite(LED_S,HIGH);
  pinMode(LED_M, OUTPUT);
  digitalWrite(LED_M,LOW);
  
  Serial.begin(57600);
}


void loop() {
    connection_test();
    digitalWrite(LED_M,HIGH);
    if (mode == 0) {
      run_millis();
    } else if (mode == 1) {
      run_micros();
    }
    digitalWrite(LED_M,LOW);
}

void connection_test() {
  while (1) {
    state1 = debounce(BTN_Test);
    if (state1 != defa) {
      if (flag1) {
        flag1 = false;
        Serial.println("t");
      }
    } else {
      flag1 = true;
    }
    if (Serial.available()) {
      userInput = Serial.read();
      if (userInput == 'm') {
          Serial.println("r");
          flag1 = true;
          mode = 0;
          break;
      }
      if (userInput == 'n') {
          Serial.println("r");
          flag1 = true;
          mode = 1;
          break;
      }
      if (userInput == 'c') {
        Serial.println("c");
      }
    }
  }
}

int debounce(int pin) {
  reading = digitalRead(pin);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
    }
  }
  lastButtonState = reading;
  return buttonState;
}

void run_millis() {
    while (1) {
        state = digitalRead(pin_in);

        if (state != LOW) {
            if (detect) {
                t1 = t2;
                t2 = millis();
                detect = false;
                T = t2 - t1;
                Serial.println(T);
            }
        } else {
            detect = true;
        }

        if(Serial.available()> 0){ 
            userInput = Serial.read();
            if (userInput == 's'){
                Serial.println("Off");
                break;
            }
        }
    }
}

void run_micros() {
    while (1) {
        state = digitalRead(pin_in);

        if (state != LOW) {
            if (detect) {
                t1 = t2;
                t2 = micros();
                detect = false;
                T = t2 - t1;
                Serial.println(T);
            }
        } else {
            detect = true;
        }

        if(Serial.available()> 0){ 
            userInput = Serial.read();
            if (userInput == 's'){
                Serial.println("Off");
                break;
            }
        }
    }
}
