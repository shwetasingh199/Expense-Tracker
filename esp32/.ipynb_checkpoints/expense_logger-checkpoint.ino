// ======================================
// ESP32 EXPENSE LOGGER
// ======================================

#define FOOD_BUTTON 18
#define TRAVEL_BUTTON 19

void setup() {
  Serial.begin(115200);

  pinMode(FOOD_BUTTON, INPUT_PULLUP);
  pinMode(TRAVEL_BUTTON, INPUT_PULLUP);

  Serial.println("Expense Tracker Started...");
}

void loop() {

  // FOOD BUTTON PRESSED
  if (digitalRead(FOOD_BUTTON) == LOW) {
    Serial.println("Food Expense: ₹200");
    delay(500);  // debounce
  }

  // TRAVEL BUTTON PRESSED
  if (digitalRead(TRAVEL_BUTTON) == LOW) {
    Serial.println("Travel Expense: ₹500");
    delay(500);
  }
}