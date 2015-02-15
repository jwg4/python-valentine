import png

from random import randint

SIZE = 2000
white = True
black = False

def is_in_heart(x, y, r):
  if y >= 0:
    return 0 - r + y < x < r - y
  if x > 0:
    cx = r / 2
  else:
    cx = - r / 2
  rr = r / 2
  return ((x - cx)**2 + y**2) < rr**2  
    
class HeartImage:
  def __init__(self, n):
    self.size = n
    self.array = []
    for y in range(n):
      line = [ white for x in range(n) ]
      self.array.append(line)

  def get_png(self):
    return png.from_array(self.array, "L;1")

  def add_heart(self, cx, cy, r, color):
    for y in range(self.size):
      for x in range(self.size):
        if is_in_heart(x - cx, y - cy, r):
          self.array[y][x] = color

  def white_points_in_circle(self, cx, cy, r):
    ymin = max(0, cy - r)
    ymax = min(cy + r + 1, self.size)
    xmin = max(0, cx - r)
    xmax = min(cx + r + 1, self.size)
    for y in range(ymin, ymax):
      for x in range(xmin, xmax):
        if (x - cx)**2 + (y - cy)**2 < r**2:
          if self.array[y][x] == white:
            return True
    return False

  def find_nearest_white_point(self, x, y):
    max = self.size / 2
    min = 1
    while max - 1 > min:
      mid = (max + min) / 2
      if self.white_points_in_circle(x, y, mid):
        max = mid
      else:
        min = mid
    return mid

  def add_biggest_white_heart(self, x, y):
    r = self.find_nearest_white_point(x, y)
    self.add_heart(x, y, r * 0.8, white)

  def find_random_black_point(self):
    while True:
      x = randint(0, self.size - 1)
      y = randint(0, self.size - 1)
      if self.array[y][x] == black:
        return (x, y)

  def add_random_white_heart(self):
    x, y = self.find_random_black_point()
    self.add_biggest_white_heart(x, y)

  def add_random_white_hearts(self, n):
    for i in range(n):
      self.add_random_white_heart()
      print i

  def add_initial_heart(self):
    self.add_heart(self.size / 2, self.size / 2, self.size * 0.45, black)

if __name__ == "__main__":
  image = HeartImage(SIZE)
  image.add_initial_heart()
  image.add_random_white_hearts(1000)
  p = image.get_png()
  p.save("heart.png")
  