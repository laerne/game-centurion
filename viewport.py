class ViewPort:
    def __init__(self):
        self.pixel_per_unit = 60.0
        self.zoom = 1.0
        self.anchor = (0,0)
        self.anchor_orientation = (0,0)
        
    @property
    def pixel_per_unit( self ):
        return 1/self._unit_per_pixel
        
    @pixel_per_unit.setter
    def pixel_per_unit( self, ppu ):
        self._unit_per_pixel = 1/ppu
        
    @property
    def unit_per_pixel( self ):
        return self._unit_per_pixel
        
    @unit_per_pixel.setter
    def unit_per_pixel( self, upp ):
        self._unit_per_pixel = upp
    
    @property
    def zoom( self ):
        return self._zoom
        
    @zoom.setter
    def zoom( self, zoom ):
        self._zoom = zoom

    @property
    def anchor( self ):
        return self._anchor
        
    @anchor.setter
    def anchor( self, anchor ):
        self._anchor = anchor

    @property
    def anchor_orientation( self ):
        return self._anchor_orientation
        
    @anchor_orientation.setter
    def anchor_orientation( self, anchor_orientation ):
        self._anchor_orientation = anchor_orientation
    
    TOP_LEFT_ANCHOR = (0,0)
    BOTTOM_LEFT_ANCHOR = (0,1)
    TOP_RIGHT_ANCHOR = (1,0)
    BOTTOM_RIGHT_ANCHOR = (1,1)
    CENTERED_ANCHOR = (0.5,0.5)
    
    def to_world_size_from_canvas_size( self, canvas_size ):
        return tuple( map( lambda p: p * self.unit_per_pixel * self.zoom, canvas_size ) )
        
    def to_world_top_left_from_canvas_size( self, canvas_size ):
        return self.world_anchor_and_size_for_canvas_size(canvas_size)[0]
    
    def to_world_top_left_and_world_size_from_canvas_size( self, canvas_size ):
        world_size = self.to_world_size_from_canvas_size( canvas_size )
        return (( self.anchor[0] - self.anchor_orientation[0] * world_size[0],
                  self.anchor[1] - self.anchor_orientation[1] * world_size[1] ),
                world_size )
    
    def to_world_coordinate_from_canvas_coordinate( self, canvas_size, pixelPosition ):
        factor = self.unit_per_pixel * self.zoom
        return ( self.anchor[0] + ( -self.anchor_orientation[0] * canvas_size[0] + pixelPosition[0]) * factor,
                 self.anchor[1] + ( -self.anchor_orientation[1] * canvas_size[1] + pixelPosition[1]) * factor )
        
    #def to_canvas_coordinate_from_world_coordinate( self, canvas_size ):
    #    pass



