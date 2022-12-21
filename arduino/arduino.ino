const int BUF_SIZE = 4;
const int STATUS_LED = 12;
const int BUTTON_PIN_START = 25; //TODO: Set to correct pin
int src;
int dst;
char buf[BUF_SIZE + 1] = {'0', '0', '0', '0', '\0'};
boolean newData = true;
int cnt = 0;

void setup() {
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(26, OUTPUT);
  pinMode(27, OUTPUT);
  pinMode(28, OUTPUT);
  pinMode(29, OUTPUT);

  pinMode(30, OUTPUT);
  pinMode(31, OUTPUT);
  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);
  pinMode(34, OUTPUT);
  pinMode(35, OUTPUT);
  pinMode(36, OUTPUT);
  pinMode(37, OUTPUT);

  pinMode(38, OUTPUT);
  pinMode(39, OUTPUT);
  pinMode(40, OUTPUT);
  pinMode(41, OUTPUT);
  pinMode(42, OUTPUT);
  pinMode(43, OUTPUT);
  pinMode(44, OUTPUT);
  pinMode(45, OUTPUT);

  pinMode(46, OUTPUT);
  pinMode(47, OUTPUT);
  pinMode(48, OUTPUT);
  pinMode(49, OUTPUT);
  pinMode(50, OUTPUT);
  pinMode(51, OUTPUT);
  pinMode(52, OUTPUT);
  pinMode(53, OUTPUT);
  
  pinMode(STATUS_LED, OUTPUT);

  digitalWrite(22, HIGH);
  digitalWrite(23, HIGH);
  digitalWrite(24, HIGH);
  digitalWrite(25, HIGH);
  digitalWrite(26, HIGH);
  digitalWrite(27, HIGH);
  digitalWrite(28, HIGH);
  digitalWrite(29, HIGH);

  digitalWrite(30, HIGH);
  digitalWrite(31, HIGH);
  digitalWrite(32, HIGH);
  digitalWrite(33, HIGH);
  digitalWrite(34, HIGH);
  digitalWrite(35, HIGH);
  digitalWrite(36, HIGH);
  digitalWrite(37, HIGH);

  digitalWrite(38, HIGH);
  digitalWrite(39, HIGH);
  digitalWrite(40, HIGH);
  digitalWrite(41, HIGH);
  digitalWrite(42, HIGH);
  digitalWrite(43, HIGH);
  digitalWrite(44, HIGH);
  digitalWrite(45, HIGH);

  digitalWrite(46, HIGH);
  digitalWrite(47, HIGH);
  digitalWrite(48, HIGH);
  digitalWrite(49, HIGH);
  digitalWrite(50, HIGH);
  digitalWrite(51, HIGH);
  digitalWrite(52, HIGH);
  digitalWrite(53, HIGH);

  digitalWrite(STATUS_LED, LOW); // Status LED

  Serial.begin(9600);
}

void loop() {

  receive();
  process();
  checkStatus();
  delay(50);
}

void receive()
{
  static byte i = 0;
  char recv;

  while (Serial.available() && newData == false)
  {
    recv = Serial.read();
    buf[i] = recv;
    i++;
    if (i >= 4)
    {
      buf[4] = '\0';
      i = 0;
      newData = true;
    }
  }
}

void process()
{
  if (newData)
  {
    char from[3];
    char to[3];
    for (int i = 0; i < 2; i++)
    {
      from[i] = buf[i];
      to[i] = buf[i + 2];
    }
    from[2] = '\0';
    to[2] = '\0';

    src = atoi(from);
    dst = atoi(to);

    if (src == 99) // set single pin
    {
      int value = 0;
      int offset = dst;
      if (dst >= 10)
      {
        value = 1;
        offset = offset - 10;
      }
      int pin = BUTTON_PIN_START + offset; // ten consecutive pins starting at BUTTON_PIN_START can set (if src == 99 --> dst = AB --> A: 0 (off) or 1 (on); B: 0-9 (offset to find actual pin) 
      
      set(pin, value);
    }
    else // set and unset a pair of pins
    {
      toggle(src, dst);
    }

    newData = false;
    for (int i = 0; i < BUF_SIZE; i++)
    {
      buf[i] = '0';
    }
  }
}

void toggle(int src, int dst)
{
  //delay(75);
  digitalWrite(src, LOW);
  digitalWrite(dst, LOW);
  delay(50);
  digitalWrite(src, HIGH);
  digitalWrite(dst, HIGH);
}

void set(int pin, int val)
{
  if (val)
  {
    digitalWrite(pin, HIGH);
  }
  else
  {
    digitalWrite(pin, LOW);
  }
}

void checkStatus()
{
  cnt++;
  if (cnt == 20)
  {
    digitalWrite(STATUS_LED, HIGH);
  }
  else if (cnt == 40)
  {
    if (!Serial)
    {
      Serial.end();
      delay(1000);
      Serial.begin(9600);
    }
    digitalWrite(STATUS_LED, LOW);
    cnt = 0;
  }
}
