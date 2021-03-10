class Switch:
  def __init__(self, serial, src, dst):
    self.serial = serial
    self.src = src
    self.dst = dst

  def toggle(self):
      self.serial.write(self.src)
      self.serial.write(self.dst)
