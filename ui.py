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
        print('drawing canvas')

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
        
        self.entity = None
        
        self.title = gtk.Label()
        self.title.set_markup( "please click an entity" )
        self.add( self.title )
        
        self.id_label = gtk.Label( label="", xalign = 0, xpad=8 )
        self.add( self.id_label )
        
        #create tag list viewer
        #self.add( gtk.Label( label="<b>Tags</b>", use_markup = True, xalign = 0, xpad=8) )
        
        self.tag_store = gtk.ListStore( str, str )
        self.tag_tree_view = gtk.TreeView( model = self.tag_store )
        self.tag_tree_view.append_column( gtk.TreeViewColumn(
                    "Tag",
                    gtk.CellRendererText(),
                    text=0 ) )
        tag_value_cell = gtk.CellRendererText( editable=True )
        self.tag_tree_view.append_column( gtk.TreeViewColumn(
                    "Value",
                    tag_value_cell,
                    text=1 ) )
        tag_value_cell.connect( 'edited', self.on_tag_value_edited )
        #self.tag_tree_view.set_headers_visible( False )
        self.add( self.tag_tree_view )

        #create property list viewer
        #self.add( gtk.Label( label="<b>Properties</b>", use_markup = True, xalign = 0, xpad=8) )
        
        self.property_store = gtk.ListStore( str, int, str )
        self.property_tree_view = gtk.TreeView( model = self.property_store )
        self.property_tree_view.append_column( gtk.TreeViewColumn(
                    "Property",
                    gtk.CellRendererText(),
                    text=0 ) )
        self.property_tree_view.append_column( gtk.TreeViewColumn(
                    "Value",
                    gtk.CellRendererText( editable=True ),
                    text=1 ) )
        self.property_tree_view.append_column( gtk.TreeViewColumn(
                    "Formula",
                    gtk.CellRendererText( editable=True, style=pango.Style.ITALIC ),
                    text=2 ) )
        #self.property_tree_view.set_headers_visible( False )
        self.add( self.property_tree_view )

    
    def set_entity( self, entity, entityId = None ):
        self.entity = entity
        if self.entity.has_tag('name'):
            entityName = self.entity.get_tag('name')
        self.title.set_markup( "<span variant=\"smallcaps\" size=\"xx-large\">%s</span>" % (entityName) )
        
        if( entityId != entityName ):
            self.id_label.set_markup( "%s" % (entityId) )
        else:
            self.id_label.set_markup("")
        
        self.tag_store.clear()
        for tag_id, tag in sorted(self.entity.tags()): #FIXME find a performance-happy iterator
            self.tag_store.append( [ tag_id, tag.value ] )
            
        self.property_store.clear()
        for p_id, p in self.entity.properties():
            self.property_store.append( [ p_id, p.value, "%s" % (str(p.update_formula)) ] )
            
    def set_tag_value( self, rowPath, newTagValue ):
        tag_id = self.tag_store[rowPath][0]
        self.entity.set_tag( tag_id, newTagValue ) #TODO Use gobject-aware mutable string and connect the string 'muted' signal to the view
        self.tag_store[rowPath][1] = newTagValue
    
    def on_tag_value_edited( self, cellRenderer, rowPath, newTagValue ):
        self.set_tag_value( rowPath, newTagValue )
        
        
        

class MainWindow(gtk.Window):
    #constructors
    def __init__(self):
        gtk.Window.__init__(self, title="Game Centurion")
        
        self.features = FeatureDisplayer()
        
        self.box = gtk.Box()
        self.add(self.box)
        
        self.canvas = Canvas()
        self.box.pack_start(self.canvas, True, True, 0)
        
        self.box.pack_start(self.features, True, True, 0)
        
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
