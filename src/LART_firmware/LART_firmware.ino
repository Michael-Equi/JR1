#define pot A0

void setup() {
  Serial.begin(115200);
  Serial.println("System Init...");

  pinMode(pot, INPUT);
}

void loop() {
  int value = analogRead(pot);
  Serial.println(value);
  delay(10);
}
