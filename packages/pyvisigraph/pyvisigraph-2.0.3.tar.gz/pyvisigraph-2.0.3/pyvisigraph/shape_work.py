"""
The MIT License (MIT)

Copyright (c) 2024 Vincent Laffargue

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
import numpy as np
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
from shapely.geometry import box
from shapely.geometry import Polygon, MultiPolygon, MultiLineString, LineString
from shapely.ops import unary_union,transform,nearest_points
import matplotlib.pyplot as plt
from geopandas import sjoin
import pandas as pd
from tqdm import tqdm
from geopy.distance import geodesic
import pickle
import pyvisigraph as vg
import pyproj
import warnings

class ShapeWork(object):

    def __init__(self):
        self.graph = vg.VisiGraph()
        self.crsProj="EPSG:3857"
        self.zone=None
        self.gdf_filtered = None
        self.bufferPointNotInShape = None
        self.bufferClosestPointBuffer = None
    
    def load(self, filename):
        """Load obstacle graph and visibility graph. """
        with open(filename, 'rb') as load:
            self.graph, self.crsProj, self.zone, self.gdf_filtered, self.bufferPointNotInShape, self.bufferClosestPointBuffer = pickle.load(load)
    
    def save(self, filename):
        """Save obstacle graph and visibility graph. """
        with open(filename, 'wb') as output:
            pickle.dump((self.graph, self.crsProj, self.zone, self.gdf_filtered, self.bufferPointNotInShape, self.bufferClosestPointBuffer), output, -1)
    
    @staticmethod
    def mydistance(point1,point2):
        return geodesic(point1[::-1], point2[::-1]).meters
    
    def buildGraph(self, filepath, zone=None, shpBuffer=0, crsProj="EPSG:3857", precision=7, workers=1):
        """
        Create graph and save it in directoryPathOut/graph and prepare differente shape to test origine/destination point for calculate shortest path
        If zone=(xmin, ymin, xmax, ymax) is given : it crop it in the zone and save the zone in directoryPathOut/buffer0.shp
        shpBuffer (number in meter) : it do the graph on the buffer of the shape. This buffer will be save in directoryPathOut/buffer1.shp. Default is 0 : no buffer
        Caution : Dont use shpBuffer on large map
        crsProj : Coordinate system used to have a system in meters for buffer.
        precision : precision used for the visi_graph (must be at least 10)
        """
        self.crsProj = crsProj
        # Charger les données des contours des terres
        print("Chargement des données des contours des terres (might take 1 minute in full resolution...)")
        gdf = gpd.read_file(filepath)
        
        if precision<7:
            print("precision must be greater than or equal to 7 -> automatic change to 7...")
            precision = 7
        if not zone:
            zone = gdf.total_bounds.tolist()
        self.zone = zone
        rect = box(minx=zone[0], miny=zone[1], maxx=zone[2], maxy=zone[3])
        # Fonction pour transformer les coordonnées du rectangle
        project = pyproj.Transformer.from_crs(pyproj.CRS('EPSG:4326'), pyproj.CRS(crsProj), always_xy=True).transform
        rectCrsProj = transform(project, rect)
        
        print("Decoupage sur la zone donnée (might take 1 minute in full resolution...)")
        self.gdf_filtered = gpd.clip(gdf, rect)
        
        print("Creating buffer for short path... (fast)")
        #Creation des buffers
        if shpBuffer==0:
            gdf_buffered_shpBuffer = self.gdf_filtered
        else:
            #Projection pour des calculs de distance en mètres
            gdf_projected = self.gdf_filtered.to_crs(crsProj)
            #Appliquer le buffer de shpBuffer mètres
            gdf_buffered = gdf_projected.buffer(shpBuffer,resolution=0)
            #On coupe pour eviter des débordement
            gdf_projected = gpd.clip(gdf_buffered, rectCrsProj)
            #Convertir le tampon en GeoDataFrame
            gdf_buffered_geo = gpd.GeoDataFrame(geometry=gpd.GeoSeries(gdf_projected), crs=crsProj)
            #Reprojeter le GeoDataFrame tamponné en WGS 84
            gdf_buffered_wgs84 = gdf_buffered_geo.to_crs("EPSG:4326")
            #On recoupe pour pas depasser la zone de base : inutile
            gdf_buffered_shpBuffer = gpd.clip(gdf_buffered_wgs84, rect)
        
        #PointNotInShape : buffer de environ au max 11cm
        # Ignorer les avertissements spécifiques relatifs aux opérations géométriques sur un CRS géographique
        warnings.filterwarnings('ignore', 'Geometry is in a geographic CRS. Results from \'buffer\' are likely incorrect.')
        gdf_buffered_wgs84 = gdf_buffered_shpBuffer.buffer(1/10**6, resolution=0)
        gdf_buffered_wgs84 = gpd.clip(gdf_buffered_wgs84, rect)
        #Premiere chose, j'unifie:
        unified_geometry = unary_union(gdf_buffered_wgs84.geometry)
        self.bufferPointNotInShape = gpd.GeoDataFrame(geometry=[unified_geometry], crs=gdf_buffered_wgs84.crs)
        #closestPointBuffer
        # Effectue la différence géométrique
        self.bufferClosestPointBuffer = rect.difference(unified_geometry)
        
        #Premiere chose, j'unifie:
        unified_geometry = unary_union(gdf_buffered_shpBuffer.geometry)
        if unified_geometry.geom_type == 'Polygon':
            # Créer une liste avec un seul Polygon
            polygons = [list(unified_geometry.exterior.coords)[::-1]]
        elif unified_geometry.geom_type == 'MultiPolygon':
            # Créer une liste de listes de tuples de coordonnées pour chaque polygone
            polygons = [list(poly.exterior.coords)[::-1] for poly in unified_geometry.geoms]
        
        #Start building graph
        self.graph.build(polygons, workers=workers,precision=precision, weight=self.mydistance, opti=True, cadre=zone)
    
    def plotGraph(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        self.gdf_filtered.plot(ax=ax, color='blue', edgecolor='k', label='Original')
        
        pos = {node: node for node in self.graph.visigraph.nodes()}
        nx.draw_networkx_edges(self.graph.visigraph, pos, edge_color='red', style='dashed', alpha=1, ax=ax)
        
        plt.show()
    
    def verifier_point_sur_terre_et_corriger(self, point, point_type,nouveaux_noeuds_sur_eau):
        """
        Vérifie si un point est sur terre, le corrige si nécessaire en trouvant le point le plus proche sur l'eau,
        ajoute les deux points au graphe si nécessaire, et relie le point d'origine au point corrigé.
        """
        point_normalise=(round(point[0],self.graph.precision),
                         round(point[1],self.graph.precision))
        # Si le point est sur terre (dans bufferPointNotInShape)
        if self.bufferPointNotInShape.intersects(Point(point_normalise)).any():
            print(f"Le point {point_type} {point} se trouve trop pres de la terre ou sur la terre pour la carte utilisée... correction en cours...")
            # Trouver le point le plus proche sur l'eau
            point_le_plus_proche = nearest_points(Point(point), self.bufferClosestPointBuffer)[1]
            point_corrige = (round(point_le_plus_proche.x,self.graph.precision),
                             round(point_le_plus_proche.y,self.graph.precision))
            nouveaux_noeuds_sur_eau.append(point_corrige)
            self.graph.visigraph.add_edge(point_normalise, point_corrige, weight=self.mydistance(point_normalise, point_corrige))
        else:
            # Le point est sur l'eau et pas déjà dans le graphe, l'ajouter au graph
            nouveaux_noeuds_sur_eau.append(point_normalise)
        return point_normalise  # Retourner l'ID du noeud origine
    
    def calculer_shortest_path(self,origin_point, destination_point):
        # Ajouter les points d'origine et de destination au graphe
        nouveaux_noeuds_sur_eau = []  # Liste pour stocker les nouveaux nœuds ajoutés sur l'eau
        origin_node_id = self.verifier_point_sur_terre_et_corriger(origin_point, "de départ",nouveaux_noeuds_sur_eau)
        destination_node_id = self.verifier_point_sur_terre_et_corriger(destination_point, "d'arrivée",nouveaux_noeuds_sur_eau)
        print("nouveau noeud" + str(nouveaux_noeuds_sur_eau))
        self.graph.update(nouveaux_noeuds_sur_eau, weight=self.mydistance)

        self.lastpath = nx.shortest_path(self.graph.visigraph, source=origin_node_id, target=destination_node_id, weight='weight')
        return self.lastpath
    
    def plotPathAndOrSave(self, filename=None, show=True, path=None):
        if path:
            # Créer une LineString à partir du chemin
            path_line = LineString(path)
        else:
            # Créer une LineString à partir du chemin
            path_line = LineString(self.lastpath)
        
        # Obtenir les limites du chemin
        minx, miny, maxx, maxy = path_line.bounds
        #print(minx, miny, maxx, maxy)
        
        # Définir les tailles minimales de l'image
        taille_min_x = 0.22
        taille_min_y = 0.185
        
        # Calculer les marges nécessaires pour atteindre la taille minimale
        delta_x = max(0, taille_min_x - (maxx - minx)) / 2
        delta_y = max(0, taille_min_y - (maxy - miny)) / 2
        
        # Appliquer les marges pour garantir la taille minimale
        minx -= delta_x
        miny -= delta_y
        maxx += delta_x
        maxy += delta_y
        #print(minx, miny, maxx, maxy)
        # Ajouter 10% de marge supplémentaire après ajustement pour taille minimale
        largeur = maxx - minx
        hauteur = maxy - miny
        marge_supplementaire_x = largeur * 0.1
        marge_supplementaire_y = hauteur * 0.1
        
        minx -= marge_supplementaire_x
        miny -= marge_supplementaire_y
        maxx += marge_supplementaire_x
        maxy += marge_supplementaire_y
        
        # Ajuster les limites en fonction de la zone couverte par gdf_filtered
        minx_gdf = self.zone[0]
        miny_gdf = self.zone[1]
        maxx_gdf = self.zone[2]
        maxy_gdf = self.zone[3]
        minx = max(minx, minx_gdf)
        miny = max(miny, miny_gdf)
        maxx = min(maxx, maxx_gdf)
        maxy = min(maxy, maxy_gdf)
        #print(minx, miny, maxx, maxy)
        # Créer le rectangle ajusté et la GeoDataFrame pour le fond bleu
        rect = box(minx, miny, maxx, maxy)
        gdf_background = gpd.GeoDataFrame(geometry=[Polygon([(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)])], crs="EPSG:4326")
        
        # Clipper gdf_filtered selon les nouvelles limites
        gdf_filtered_clipped = gpd.clip(self.gdf_filtered, rect)
        
        # Créer une GeoDataFrame pour le chemin
        gdf_path = gpd.GeoDataFrame(geometry=[path_line], crs="EPSG:4326")
        
        # Afficher la carte et le chemin
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf_background.plot(ax=ax, color='#add8e6')  # Fond bleu clair pour l'eau
        gdf_filtered_clipped.plot(ax=ax, color='#A9A9A9')  # Carte en arrière-plan
        gdf_path.plot(ax=ax, color='red', linewidth=2)  # Chemin en rouge
        
        # Désactiver les axes
        ax.set_axis_off()
        #plt.show()
        # Enregistrer l'image
        if filename:
            fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
        if show:
            plt.show()
        plt.close(fig)


