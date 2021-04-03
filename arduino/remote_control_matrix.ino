const int BUF_SIZE = 4;
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

  pinMode(50, OUTPUT);

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

  digitalWrite(50, LOW); // Status LED

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

    toggle(src, dst);

    newData = false;
    for (int i = 0; i < BUF_SIZE; i++)
    {
      buf[i] = '0';
    }
  }
}

void toggle(int src, int dst)
{
  delay(25);
  digitalWrite(src, LOW);
  digitalWrite(dst, LOW);
  delay(50);
  digitalWrite(src, HIGH);
  digitalWrite(dst, HIGH);
}

void checkStatus()
{
  cnt++;
  if (cnt == 20)
  {
    digitalWrite(50, HIGH);
  }
  else if (cnt == 40)
  {
    if (!Serial)
    {
      Serial.end();
      delay(1000);
      Serial.begin(9600);
    }
    digitalWrite(50, LOW);
    cnt = 0;
  }
}
