"""
The MIT License (MIT)

Copyright (c) 2024 Vincent Laffargue
Copyright (c) 2016 Christian August Reksten-Monsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from pyvisigraph.graph import Point
from functools import cmp_to_key

CCW = 1
CW = -1
COLLINEAR = 0

def generateur_de_comparaisonhalf(point):
    def comparer(p1, p2):
        dx1=p1.x-point.x
        dy1=p1.y-point.y
        dx2=p2.x-point.x
        dy2=p2.y-point.y
        o_= dy1*dx2-dy2*dx1
        #o_=ccw(point,p2,p1)
        if o_==0:
            if dx1**2 + dy1**2 < dx2**2 + dy2**2 :
                return -1
            else:
                return 1
        else :
            return o_
    return comparer

def generateur_de_comparaison(point):
    def comparer(p1, p2):
        if (p1.y==point.y and p1.x>point.x) or p1.y>point.y :
            if (p2.y==point.y and p2.x>point.x) or p2.y>point.y:
                dx1=p1.x-point.x
                dy1=p1.y-point.y
                dx2=p2.x-point.x
                dy2=p2.y-point.y
                o_= dy1*dx2-dy2*dx1
                if o_==0:
                     if dx1**2 + dy1**2 < dx2**2 + dy2**2 :
                         return -1
                     else:
                         return 1
                else :
                    return o_
            else:
                return -1
        else :
            if (p2.y==point.y and p2.x>point.x) or p2.y>point.y:
                return 1
            else :
                dx1=p1.x-point.x
                dy1=p1.y-point.y
                dx2=p2.x-point.x
                dy2=p2.y-point.y
                o_= dy1*dx2-dy2*dx1
                if o_==0:
                     if dx1**2 + dy1**2 < dx2**2 + dy2**2 :
                         return -1
                     else:
                         return 1
                else :
                    return o_            
    return comparer

def generateur_du_test1(graph,point):
    if len(graph.get_adjacent_points(point))==2:
        p1, p2 = graph.get_adjacent_points(point)
        def test1opti(p,ccw_memory):
            if p.neverVisi:
                return False
            if ccw_memory[0][1]*ccw_memory[1][1]<0:
                return False
            if ccw(p1,point,p)*ccw(p2,point,p)<0:
                return False
            return True
    else:
        def test1opti(p,ccw_memory):
            if p.neverVisi:
                return False
            if len(ccw_memory)==2:
                if ccw_memory[0][1]*ccw_memory[1][1]<0:
                    return False
            return True
    return test1opti

def visible_vertices(point, graph, scan='full', opti=False):
    """Returns list of Points in graph visible by point.

    If origin and/or destination Points are given, these will also be checked
    for visibility. scan 'full' will check for visibility against all points in
    graph, 'half' will check for visibility against half the points. This saves
    running time when building a complete visibility graph, as the points
    that are not checked will eventually be 'point'.
    """
    if point.neverVisi:
        return []
    if opti:
        test1 = generateur_du_test1(graph,point)
        test2 = lambda visible : True       
    else:
        test1 = lambda p,ccw_memory : not p.neverVisi
        test2 = lambda visible : not visible
    edges = graph.get_edges()
    points = graph.get_points()
    maxX=graph.maxX+10
    points.remove(point)
    if scan == 'half':
        newpoints=[]
        for p in points:
            if (p.y==point.y and p.x>point.x) or p.y>point.y:
                newpoints.append(p)
        comparer = generateur_de_comparaisonhalf(point)
        points = sorted(newpoints, key=cmp_to_key(comparer))
    else:
        comparer = generateur_de_comparaison(point)
        points = sorted(points, key=cmp_to_key(comparer))
    
    # Initialize open_edges with any intersecting edges on the half line from
    # point along the positive x-axis
    open_edges = OpenEdges()
    point_inf = Point(maxX, point.y,precision=-1)
    for edge in edges:
        if ((edge.p1.x>point.x or edge.p2.x>point.x) and (edge.p1.y<point.y or edge.p2.y<point.y)
        and (edge.p1.y>point.y or edge.p2.y>point.y)):
            o1= ccw(edge.p1,edge.p2,point)
            o2= ccw(edge.p1,edge.p2,point_inf)
            if o1*o2<0:
                open_edges.insert_begining(point, point_inf, edge)
    
    visible = []
    prev = None
    prev_visible = None
    for p in points:
        #Optimisation: je conserve les resultats de ccw
        ccw_memory=[(edge,ccw(point, p, edge.get_adjacent(p))) for edge in graph[p]]
        # Update open_edges - remove clock wise edges incident on p
        if p.y!=point.y or p.x<point.x:
            for edge,ccw1 in ccw_memory:
                if ccw1 == CW:
                    open_edges.delete(point, p, edge)
        
        # Check if p is visible from point
        is_visible = False
        #if point will be never visi : do nothing
        if test1(p,ccw_memory):
            # ...Non-collinear points
            if prev is None or ccw(point, prev, p) != COLLINEAR or not on_segment(point, prev, p):
                if len(open_edges) == 0:
                    is_visible = True
                else:
                    edgetest=open_edges.smallest()
                    o1= ccw(edgetest.p1,edgetest.p2,point)
                    o2= ccw(edgetest.p1,edgetest.p2,p)
                    if o1*o2>0:
                        is_visible = True
                # Check if the visible edge is interior to its polygon
                if not opti:
                    if is_visible and p not in graph.get_adjacent_points(point):
                        if edge_in_polygon(point, p, graph,maxX):
                            is_visible = False
            
            # ...For collinear points, if previous point was not visible, p is not
            elif test2(prev_visible):
                is_visible = False
            # ...For collinear points, if previous point was visible, need to check
            # that the edge from prev to p does not intersect any open edge.
            else:
                is_visible = True
                for edge in open_edges:
                    if prev not in edge:
                        o1= ccw(edge.p1,edge.p2,prev)
                        o2= ccw(edge.p1,edge.p2,p)
                        if o1*o2<0:
                            is_visible = False
                            break
                if is_visible and p not in graph.get_adjacent_points(prev):
                    if edge_in_polygon(prev, p, graph,maxX):
                        is_visible = False
        
        if is_visible: 
            visible.append(p)
        
        # Update open_edges - Add counter clock wise edges incident on p
        for edge,ccw1 in ccw_memory:
            if ccw1 == CCW:
                 open_edges.insert(point, p, edge)
        
        prev = p
        prev_visible = is_visible
    return visible

def polygon_crossing(p1, poly_edges,maxX):
    """Returns True if Point p1 is internal to the polygon. The polygon is
    defined by the Edges in poly_edges. Uses crossings algorithm and takes into
    account edges that are collinear to p1."""
    #print(poly_edges)
    p2 = Point(maxX+10, p1.y,precision=-1)
    intersect_count = 0
    for edge in poly_edges:
        if p1.y < edge.p1.y and p1.y < edge.p2.y: continue
        if p1.y > edge.p1.y and p1.y > edge.p2.y: continue
        if p1.x > edge.p1.x and p1.x > edge.p2.x: continue
        # Deal with points collinear to p1
        edge_p1_collinear = (edge.p1.y == p1.y)
        edge_p2_collinear = (edge.p2.y == p1.y)
        if edge_p1_collinear and edge_p2_collinear: continue
        if edge_p1_collinear or edge_p2_collinear:
            collinear_point = edge.p1 if edge_p1_collinear else edge.p2
            if collinear_point.x > p1.x and edge.get_adjacent(collinear_point).y > p1.y:
                    intersect_count += 1
        else :
            o3=ccw(edge.p1, edge.p2, p1)
            o4=ccw(edge.p1, edge.p2, p2)
            if o3 != o4:
              intersect_count += 1
    if intersect_count % 2 == 0:
        return False
    return True

def edge_in_polygon(p1, p2, graph,maxX):
    """Return true if the edge from p1 to p2 is interior to any polygon
    in graph."""
    if p1.polygon_id != p2.polygon_id:
        return False
    if p1.polygon_id == -1 or p2.polygon_id == -1:
        return False
    mid_point = Point((p1.x + p2.x) // 2, (p1.y + p2.y) // 2,precision=-1)
    return polygon_crossing(mid_point, graph.polygons[p1.polygon_id],maxX)

def ccw(A, B, C):
    """Return 1 if counter clockwise, -1 if clock wise, 0 if collinear """
    area = (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)
    if area > 0: return 1
    if area < 0: return -1
    return 0

def on_segment(p, q, r):
    """Given three colinear points p, q, r, the function checks if point q
    lies on line segment 'pr'."""
    if (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)):
        if (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)):
            return True
    return False

class OpenEdges(object):
    def __init__(self):
        self._open_edges = []

    def insert(self, p1, p2, edge):
        self._open_edges.insert(self._index(p1, p2, edge), edge)

    def delete(self, p1, p2, edge):
        index = self._index(p1, p2, edge) - 1
        if self._open_edges[index] == edge:
            del self._open_edges[index]
        else:
            raise ValueError("le coté correspond pas : ERROR.")

    def smallest(self):
        return self._open_edges[0]
    
    def _less_than_begining(self, p1, p2, edge1, edge2):
        o1 = ccw(edge1.p1, edge1.p2, edge2.p1)
        o2 = ccw(edge1.p1, edge1.p2, edge2.p2)
        if o1+o2!=0:
            return ccw(edge1.p1, edge1.p2, p1)*(o1+o2)<0
        else:
            if o1==0:
                raise ValueError("Cas exclu : deux segments se superposent : préparer votre carte!!!!.")
            o3=ccw(edge2.p1, edge2.p2, edge1.p1)
            if o3==0:
                o3=ccw(edge2.p1, edge2.p2, edge1.p2)
            return ccw(edge2.p1, edge2.p2, p1)*o3>0
    
    def insert_begining(self, p1, p2, edge):
        self._open_edges.insert(self._index_begining(p1, p2, edge), edge)
    
    def _index_begining(self, p1, p2, edge):
        lo = 0
        hi = len(self._open_edges)
        while lo < hi:
            mid = (lo+hi)//2
            if self._less_than_begining(p1, p2, edge, self._open_edges[mid]):
                hi = mid
            else:
                lo = mid + 1
        return lo
    
    def _less_than_normal(self, p1, p2, edge1, edge2):
        """Return True if edge1 is smaller than edge2, False otherwise."""
        if edge1 == edge2:
            return False
        if p2 in edge2:
            o1 = ccw(p2,edge2.get_adjacent(p2),p1)
            o2 = ccw(p2,edge2.get_adjacent(p2),edge1.get_adjacent(p2))
            return o1*o2>0
        o1 = ccw(edge1.p1, edge1.p2, edge2.p1)
        o2 = ccw(edge1.p1, edge1.p2, edge2.p2)
        if o1+o2!=0:
            return ccw(edge1.p1, edge1.p2, p1)*(o1+o2)<0
        else:
            if o1==0:
                raise ValueError("Cas exclu : deux segments se superposent : préparer votre carte!!!!.")
            o3=ccw(edge2.p1, edge2.p2, edge1.p1)
            if o3==0:
                o3=ccw(edge2.p1, edge2.p2, edge1.p2)
            return ccw(edge2.p1, edge2.p2, p1)*o3>0

    def _index(self, p1, p2, edge):
        lo = 0
        hi = len(self._open_edges)
        while lo < hi:
            mid = (lo+hi)//2
            if self._less_than_normal(p1, p2, edge, self._open_edges[mid]):
                hi = mid
            else:
                lo = mid + 1
        return lo

    def __len__(self):
        return len(self._open_edges)

    def __getitem__(self, index):
        return self._open_edges[index]
    
    def getAll(self):
        return self._open_edges
