    cos_a = math.cos( path.angle )
    sin_a = math.sin( path.angle )
    rotation_a = cos_a + sin_a * 1j
    rotation_minus_a = rotation_a.conjugate()
    
    # 1. compute the center of the ellipsis and the angle of the start point and end point
    #   1.1 change to an axis-aligned reference system
    axisaligned_start = rotation_minus_a * path.start 
    axisaligned_end = rotation_minus_a * path.end





    start_angle = radians(self.theta)
    cos_sa = cos(start_angle)
    sin_sa = sin(start_angle)
    point_sa = cos_sa * path.radius.real + sin_sa * path.radius.imag 1j
    
    end_angle = radians(self.theta + self.delta)
    cos_ea = cos(end_angle)
    sin_ea = sin(end_angle)
    point_ea = cos_ea * path.radius.real + sin_ea * path.radius.imag 1j
    
    path_angle = radians(path.rotation)
    cos_r = cos( path_angle )
    sin_r = sin( path_angle )
    rot = cos_r + sin_r * 1j

class Rectangle:
    def __init__(self,x,y,w,h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        
    def getX(self):
        return self._x
    def getY(self):
        return self._y
    def getWidth(self):
        return self._w
    def getHeight(self):
        return self._h
    def set(self,x):
        self._x = x
    def setY(self,y):
        self._y = y
    def setWidth(self,w):
        self._w = w
    def setHeight(self,h):
        self._h = h
        
    x = property( getX, setX, doc=' the x-value of the bottom-left corner' )
    y = property( getY, setY, doc=' the y-value of the bottom-left corner' )
    width = property( getWidth, setWidth, doc=' the y-value of the bottom-left corner' )
    height = property( getHeight, setHeight, doc=' the y-value of the bottom-left corner' )
