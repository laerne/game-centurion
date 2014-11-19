import world
import sympy

w = world.World()
l=list(w.parse_and_add('zones.yaml').items())

for i in range(-10,-1):
    z=l[i]
    print(z[0],end=':\n')
    for t,tv in z[1].tags():
        print( "    %s : %s" % (t,tv.value) )
    for p,pvu in z[1].properties():
        print( "    %s : %s --( %s )--> %s" % (p,pvu.value,pvu.update_formula,pvu._update_function(pvu.value)) )
