class Switch:
  def __init__(self, serial, src, dst):
    self.serial = serial
    self.src = src
    self.dst = dst

  def toggle():
      serial.write(src)
      serial.write(dst)
