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
from timeit import default_timer
from sys import stdout, version_info
from multiprocessing import Pool
from tqdm import tqdm
from warnings import warn
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from pyvisigraph.graph import Graph, Edge, Point
from pyvisigraph.visible_vertices import visible_vertices

PYTHON3 = version_info[0] == 3
if PYTHON3:
    xrange = range
    import pickle
else:
    import cPickle as pickle


class VisiGraph(object):

    def __init__(self):
        self.graph = None
        self.visigraph = nx.Graph()
        self.precision = None
        self.opti = False

    def load(self, filename):
        """Load obstacle graph and visibility graph. """
        with open(filename, 'rb') as load:
            self.graph, self.visigraph, self.precision, self.opti = pickle.load(load)
    
    def save(self, filename):
        """Save obstacle graph and visibility graph. """
        with open(filename, 'wb') as output:
            pickle.dump((self.graph, self.visigraph, self.precision, self.opti), output, -1)

    def build(self, polygons, precision,weight=None, workers=1, status=True, opti=False , cadre=None): 
        """Build visibility graph based on a list of polygons.

        Variable polygons must be a list of polygons, where each polygon is a list of
        in-order (counter clockwise) Points. It only one polygon,
        it must still be a list in a list, i.e. [[Point(0,0), Point(2,0),
        Point(2,-1)]].
        The variable "precision" must be a positive integer. The recommended number is 7. This allows for accuracy to within a centimeter without unnecessarily burdening the calculations. This value is not the default to always be aware that the algorithm will always truncate the given coordinates to 10^-precision degree precision. 
        Take advantage of processors with multiple cores by setting workers to
        the number of subprocesses you want. Defaults to 1, i.e. no subprocess
        will be started.
        Set status=False to turn off the statusbar when building.
        opti : if True -> register only necessary visibility edge for shortest path
        cadre : (xmin, ymin, xmax, ymax) : dont take edge on cadre : only works in Opti mode
        """
        if not opti and cadre:
           print('cadre only works in opti mode')
           print('**** Opti mode activated****')
           opti = True
        if weight:
            addGraph = lambda p1, p2: self.visigraph.add_edge(p1, p2, weight=weight(p1, p2))
        else:
            addGraph = lambda p1, p2: self.visigraph.add_edge(p1, p2)
        self.precision = precision
        self.graph = Graph(polygons, precision, opti, cadre)
        self.visigraph = nx.Graph()
        self.opti = opti
        self.graph.checkGeometry()
        points = self.graph.get_points()
        batch_size = 10
        print("Starting building graph of visibility...")
        if workers == 1:
            for batch in tqdm([points[i:i + batch_size]
                               for i in xrange(0, len(points), batch_size)],
                            disable=not status):
                for edge in _visi_graph(self.graph, batch, opti):
                    point1=(edge.p1.x/(2*10**precision), edge.p1.y/(2*10**precision))
                    point2=(edge.p2.x/(2*10**precision), edge.p2.y/(2*10**precision))
                    addGraph(point1,point2)
        else:
            pool = Pool(workers)
            batches = [(self.graph, points[i:i + batch_size], opti)
                       for i in xrange(0, len(points), batch_size)]

            results = list(tqdm(pool.imap(_visi_graph_wrapper, batches), total=len(batches),
                disable=not status))
            for result in results:
                for edge in result:
                    point1=(edge.p1.x/(2*10**precision), edge.p1.y/(2*10**precision))
                    point2=(edge.p2.x/(2*10**precision), edge.p2.y/(2*10**precision))
                    addGraph(point1,point2)
            return results

    def update(self, points, weight=None):
        """Update visgraph by checking visibility of Points in list points."""
        if weight:
            addGraph = lambda p1, p2: self.visigraph.add_edge(p1, p2, weight=weight(p1, p2))
        else:
            addGraph = lambda p1, p2: self.visigraph.add_edge(p1, p2)
        Newpoint = []
        for p_ in points:
            point_ = Point(p_[0],p_[1],self.precision)
            if point_ not in self.graph.graph :
                Newpoint.append(point_)
                self.graph.graph[point_]
                self.graph.maxX = max(self.graph.maxX,point_.x)
        for p in Newpoint:
            for v in visible_vertices(p, self.graph, scan='full', opti = self.opti):
                point1=(p.x/(2*10**self.precision), p.y/(2*10**self.precision))
                point2=(v.x/(2*10**self.precision), v.y/(2*10**self.precision))
                addGraph(point1,point2)
    
    def plotGraphAndOrSave(self,polys=None, filename=None, show=True):
        fig, ax = plt.subplots()
        if polys:
            ## Visualiser les polygones
            for poly in polys:
                polygon = patches.Polygon(poly, closed=True, fill=None, edgecolor='black')
                ax.add_patch(polygon)
        ## Visualiser le graph de visibilite
        pos = {node: node for node in self.visigraph.nodes()}
        nx.draw_networkx_edges(self.visigraph, pos, edge_color='red', style='dashed', alpha=1, ax=ax)
        # Enregistrer l'image
        if filename:
            fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
        # Montrer la figure
        if show:
            plt.show()


def _visi_graph_wrapper(args):
    try:
        return _visi_graph(*args)
    except KeyboardInterrupt:
        pass

def _visi_graph(graph, points,opti):
    visible_edges = []
    for p1 in points:
        for p2 in visible_vertices(p1, graph, scan='half',opti = opti):
            visible_edges.append(Edge(p1, p2))
    return visible_edges
