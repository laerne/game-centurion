import svg.path
import math
import sympy
import cairo

def ensureIsCurrentPoint( context, point ):
    p = ( point.real, point.imag )
    if context.get_current_point() != p:
        context.move_to( *p )

def traceSvgPath( path, context ):
    segments = path
    
    for segment in segments:
        segment_type = type(segment)
        if segment_type == svg.path.Line:
            traceSvgLine( segment, context )
        elif segment_type == svg.path.CubicBezier:
            traceSvgCubicBezier( segment, context )
        elif segment_type == svg.path.QuadraticBezier:
            traceSvgQuadraticBezier( segment, context )
        elif segment_type == svg.path.Arc:
            traceSvgEllipticArc( segment, context )

def traceSvgCubicBezier( segment, context ):
    ensureIsCurrentPoint( context, segment.start )
    context.curve_to(
            segment.control1.real, segment.control1.imag,
            segment.control2.real, segment.control2.imag,
            segment.end.real, segment.end.imag
            )

def traceSvgQuadraticBezier( segment, context ):
    control1 = ( segment.start + 2 * segment.control ) / 3
    control2 = ( segment.end   + 2 * segment.control ) / 3
    ensureIsCurrentPoint( context, segment.start )
    context.curve_to(
            control1.real, control1.imag,
            control2.real, control2.imag,
            segment.end.real, segment.end.imag,
            )

def traceSvgLine( segment, context ):
    ensureIsCurrentPoint( context, segment.start )
    context.line_to( segment.end.real, segment.end.imag )
    
def traceSvgEllipticArc( segment, context ):
    start_angle = math.radians(self.theta)
    end_angle = math.radians(self.theta + self.delta)
    
    context.save()
    
    context.translate( segment.center.real, segment.center.imag )
    context.rotate( radians(segment.rotation) )
    context.scale( segment.radius.real, segment.radius.imag )
    context.arc( 0.0, 0.0, 1.0, start_angle, end_angle )
    
    context.restore()
    
    context.move_to( segment.end )
