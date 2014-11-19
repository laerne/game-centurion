#!/usr/bin/env python3
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import Pango as pango
import cairo
import world
import tracepath

class Canvas(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_size_request(600,400)
        self.connect('draw',Canvas.on_draw)
        self.bottom_left_position = (0.0,0.0)
        self.world = None
        
    def on_realize(self, emitter, event):
        pass
        
    def on_configure_event(self, emitter, event):
        pass
    
    def on_draw(self,context):

        # clear widget
        context.set_source_rgb( 0.1, 0.0, 0.1 )
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        
        # paint widget
        if self.world:
            context.set_operator(cairo.OPERATOR_OVER)
            context.set_line_width(0.5)
            context.set_line_join(cairo.LINE_JOIN_ROUND)
            context.set_source_rgb( 1.0, 1.0, 1.0 )
            for zone_id,zone in self.world.zones():
                tracepath.traceSvgPath( zone.path, context )
                context.stroke()
                
        
    def setWorld(self, world):
        self.world = world

class FeatureDisplayer( gtk.Box ):
    def __init__( self ):
        gtk.Box.__init__( self, orientation=gtk.Orientation.VERTICAL )
        
        self._entity = None
        
        self.title = gtk.Label()
        self.title.set_markup( "please click an entity" )
        self.add( self.title )
        
        self.id_label = gtk.Label( label="", xalign = 0, xpad=8 )
        self.add( self.id_label )
        self._connections = []
        
        #create tag list viewer
        
        self.tag_store = gtk.ListStore( str, str )
        self.tag_tree_view = gtk.TreeView( model = self.tag_store )
        self.tag_tree_view.append_column( gtk.TreeViewColumn(
                    "Tag",
                    gtk.CellRendererText(),
                    text=0 ) )
        tag_value_cell = gtk.CellRendererText( editable=True )
        tag_value_cell.connect( 'edited', self.on_tag_value_edited )
        self.tag_tree_view.append_column( gtk.TreeViewColumn(
                    "Value",
                    tag_value_cell,
                    text=1 ) )
        self.add( self.tag_tree_view )

        #create property list viewer
        self.property_store = gtk.ListStore( str, int, str )
        self.property_tree_view = gtk.TreeView( model = self.property_store )
        self.property_tree_view.append_column( gtk.TreeViewColumn(
                    "Property",
                    gtk.CellRendererText(),
                    text=0 ) )
        property_value_cell = gtk.CellRendererText( editable=True )
        property_value_cell.connect( 'edited', self.on_property_value_edited )
        self.property_tree_view.append_column( gtk.TreeViewColumn(
                    "Value",
                    property_value_cell,
                    text=1 ) )
        self.property_tree_view.append_column( gtk.TreeViewColumn(
                    "Formula",
                    gtk.CellRendererText( editable=True, style=pango.Style.ITALIC ),
                    text=2 ) )
        self.add( self.property_tree_view )
        
    def remove_entity( self ):
        for feature, connection_id in self._connections:
            feature.disconnect( connection_id )
        self._connections = []
        self._entity = None
    
    def set_entity( self, entity, entityId = None ):
        #if sef.entity != None:
        #    self.remove_entity()
        self._entity = entity
        if self._entity.has_tag('name'):
            entityName = self._entity.get_tag('name')
        self.title.set_markup( "<span variant=\"smallcaps\" size=\"xx-large\">%s</span>" % (entityName) )
        
        if( entityId != entityName ):
            self.id_label.set_markup( "%s" % (entityId) )
        else:
            self.id_label.set_markup("")
        
        self.tag_store.clear()
        for tag_id, tag in sorted(self._entity.tags()): #FIXME find a performance-happy iterator
            tag_iterator = self.tag_store.append( [ tag_id, tag.value ] )
            tag_path = self.tag_store.get_path( tag_iterator )
            
            tag_connection_id = tag.feature.connect( 'mutated', self.on_new_tag_value, tag_path )
            if tag_id == 'name' :
                name_connection_id = tag.feature.connect( 'mutated', self.on_new_name )
            
            self._connections.append(( tag.feature, tag_connection_id ))
            
        self.property_store.clear()
        for property_id, property in sorted(self._entity.properties()):
            property_iterator = self.property_store.append( [ property_id, property.value, "%s" % (str(property.update_formula)) ] )
            property_path = self.property_store.get_path( property_iterator )
            
            property_connection_id = property.feature.connect( 'mutated', self.on_new_property_value, property_path )
            
            #self._connections.append( feature, property_connection_id )
            
    #tag handler
    def set_tag_value( self, rowPath, newTagValue ):
        tag_id = self.tag_store[rowPath][0]
        self._entity.set_tag( tag_id, newTagValue ) #TODO Use gobject-aware mutable string and connect the string 'muted' signal to the view
    
    def on_tag_value_edited( self, emitter, rowPath, newTagValue ):
        self.set_tag_value( rowPath, newTagValue )
    
    def on_new_tag_value( self, emitter, newValue, tagPath ):
        print( tagPath, "===", repr(tagPath), "|||", repr(emitter) )
        self.tag_store[tagPath][1] = newValue
        
    def on_new_name( self, emitter, newName ):
        self.title.set_markup( "<span variant=\"smallcaps\" size=\"xx-large\">%s</span>" % (newName) )

    #property value handle
    def set_property_value( self, rowPath, newpropertyValue ):
        property_id = self.property_store[rowPath][0]
        self._entity.set_property( property_id, newpropertyValue )
    
    def on_property_value_edited( self, emitter, rowPath, newpropertyValue ):
        self.set_property_value( rowPath, newpropertyValue )
    
    def on_new_property_value( self, emitter, newValue, propertyPath ):
        print( propertyPath, "===", repr(propertyPath), "|||", repr(emitter) )
        self.property_store[propertyPath][1] = newValue
        
    #property formula handler
    def set_property_formula( self, rowPath, newpropertyFormula ):
        property_id = self.property_store[rowPath][0]
        self._entity.set_property( property_id, newpropertyFormula )
    
    def on_property_formula_edited( self, emitter, rowPath, newpropertyFormula ):
        self.set_property_formula( rowPath, newpropertyFormula )
    
    def on_new_property_formula( self, emitter, newFormula, propertyPath ):
        print( propertyPath, "===", repr(propertyPath), "|||", repr(emitter) )
        self.property_store[propertyPath][1] = newFormula
        
        
        
        
class EventList(gtk.Table):
    def __init__(self):
        gtk.Table.__init__( self, n_rows=1, homogeneous=False )
        self.attach( gtk.Button( label='a₀' ), 0, 1, 0, 1, xoptions=0, yoptions=0 )
        self.attach( gtk.Button( label='b?' ), 1, 2, 0, 1, xoptions=0, yoptions=0 )
        self.attach( gtk.Button( label='c²' ), 2, 3, 0, 1, xoptions=0, yoptions=0 )

        

class MainWindow(gtk.Window):
    #constructors
    def __init__(self):
        gtk.Window.__init__(self, title="Game Centurion")
        
        self.vertical_box = gtk.VBox()
        self.add(self.vertical_box)
        
        self.event_list = EventList()
        self.vertical_box.pack_start(self.event_list, expand=False, fill=False, padding=0)
        
        self.horizontal_box = gtk.HBox()
        self.horizontal_box.vexpand = True
        self.vertical_box.pack_start(self.horizontal_box, expand=True, fill=True, padding=0)
        
        self.canvas = Canvas()
        self.horizontal_box.pack_start(self.canvas, expand=True, fill=True, padding=0)
        
        self.features = FeatureDisplayer()
        self.horizontal_box.pack_start(self.features, expand=True, fill=True, padding=0)
        
        self.connect('delete-event', self.on_quit)
    
    #properties
    def setWorld(self, world):
        self.world = world
        self.canvas.setWorld(world)
        
        #TODO Remove this debug code when the canvas selection works
        zn, z = next(world.zones())
        self.features.set_entity(z,zn)
        
    #signal handlers
    def on_quit(self, window, event):
        gtk.main_quit()

if __name__ == '__main__':
    w = MainWindow()
    w.show_all()
    gtk.main()
