// Arduino Code for Robotics Exam 1
String inputString = "";
bool isStringComplete = false;

void setup() {
  Serial.begin(9600);
  inputString.reserve(200);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (isStringComplete) {
    if (inputString.equals("LED ON")) {
      Serial.println("LED On");
      digitalWrite(LED_BUILTIN, HIGH);
    } else if (inputString.equals("LED OFF")) {
      Serial.println("LED Off");
      digitalWrite(LED_BUILTIN, LOW);
    } else if (inputString.startsWith("FLASH ")) {
      String args = inputString.substring(6);
      int spaceIndex = args.indexOf(" ");
      int numFlashes = args.substring(0, spaceIndex).toInt();
      int periodMs = args.substring(spaceIndex + 1).toInt();
      Serial.print("Flashes = ");
      Serial.print(numFlashes);
      Serial.print(" PeriodMs = ");
      Serial.println(periodMs);
      for (int i = 0; i < numFlashes; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(periodMs / 2);
        digitalWrite(LED_BUILTIN, LOW);
        delay(periodMs / 2);
      }
    } else {
      Serial.print("Unknown command --> ");
      Serial.println(inputString);
    }
    inputString = "";
    isStringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      isStringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}