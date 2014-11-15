import world
import sympy

w = world.World()
l=list(w.parse_and_add('map.svg','zones.yaml').items())

for i in range(-10,-1):
    z=l[i]
    print(z[0],end=':\n')
    for t,tv in z[1].tags.items():
        print( "    %s : %s" % (t,tv) )
    for p,pvu in z[1].properties.items():
        print( "    %s : %s --( %s )--> %s" % (p,pvu.value,pvu.update_formula,pvu.update_function(pvu.value)) )
