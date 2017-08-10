import numpy as np
import matplotlib.cm as cm
from scipy.spatial import Delaunay
from plotly.graph_objs import *

def map_z2color(zval, colormap, vmin, vmax):
    #map the normalized value val to a corresponding color in the mpl colormap
    
    if vmin>=vmax:
        raise ValueError('incorrect relation between vmin and vmax')
    t=(zval-vmin)/float((vmax-vmin))#normalize val
    C=map(np.uint8, np.array(colormap(t)[:3])*255)
    #convert to a Plotly color code:
    return 'rgb'+str((C[0], C[1], C[2]))

def mpl_to_plotly(cmap, pl_entries):
    h=1.0/(pl_entries-1)
    pl_colorscale=[]
    for k in range(pl_entries):
        C=map(np.uint8, np.array(cmap(k*h)[:3])*255)
        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
    return pl_colorscale

def plotly_trisurf(x, y, z, simplices, colormap=cm.RdBu, showcolorbar=False, plot_edges=None):
    #x, y, z are lists of coordinates of the triangle vertices 
    #simplices are the simplices that define the triangulation;
    #simplices  is a numpy array of shape (no_triangles, 3)
    #insert here the  type check for input data
    
    points3D=np.vstack((x,y,z)).T
    tri_vertices= points3D[simplices]# vertices of the surface triangles  
    zmean=tri_vertices[:, :, 2].mean(-1)# mean values of z-coordinates of the
                                        #triangle vertices
      
    min_zmean, max_zmean=np.min(zmean), np.max(zmean)
    
    facecolor=[map_z2color(zz,  colormap, min_zmean, max_zmean) for zz in zmean] 
    I,J,K=zip(*simplices)
    
    triangles=Mesh3d(x=x,
                     y=y,
                     z=z,
                     facecolor=facecolor, 
                     i=I,
                     j=J,
                     k=K,
                     name=''
                    )
    
    if showcolorbar==True:
        pl_colorsc=mpl_to_plotly(colormap,11)
        # define a fake Scatter3d trace in order to enable displaying the colorbar for the trisurf
        
        colorbar=Scatter3d(x=x[:2],
                           y=y[:2],
                           z=z[:2],
                           mode='markers',
                           marker=dict(size=0.1, color=[min_zmean, max_zmean], 
                                      colorscale=pl_colorsc, showscale=True),
                             hoverinfo='None'
                          )
    
    
    if plot_edges is None: # the triangle sides are not plotted 
        if  showcolorbar is True:
            return Data([colorbar, triangles])
        else: 
            return  Data([triangles])
    else:#plot edges
        #define the lists Xe, Ye, Ze, of x, y, resp z coordinates of edge end points for each triangle
        #None separates data corresponding to two consecutive triangles
        Xe=[]
        Ye=[]
        Ze=[]
        for T in tri_vertices:
            Xe+=[T[k%3][0] for k in range(4)]+[ None]
            Ye+=[T[k%3][1] for k in range(4)]+[ None]
            Ze+=[T[k%3][2] for k in range(4)]+[ None]
       
        #define the lines to be plotted
        lines=Scatter3d(x=Xe,
                        y=Ye,
                        z=Ze,
                        mode='lines',
                        line=Line(color= 'rgb(50,50,50)', width=1.5)
               )
        if  showcolorbar is True:
            return Data([colorbar, triangles, lines])
        else: 
            
            return Data([triangles, lines])

def gd_profSurf(x, y, z, projZ, simplices, colormap=cm.RdBu, showcolorbar=False, plot_edges=True,triColor='rgb(50,50,50)'):
        
    I,J,K=zip(*simplices)
    
    triColors = np.random.randint(0, high=100,size=(len(simplices)))
    facecolors=[map_z2color(zz,  cm.RdBu, 0, 100) for zz in triColors]
    
    triangles=Mesh3d(x=x,
                     y=y,
                     z=np.tile(projZ,len(x)),
                     facecolor=facecolors, 
                     i=I,
                     j=J,
                     k=K,
                     name=''
                    )
    

    if plot_edges is None: # the triangle sides are not plotted 
        if  showcolorbar is True:
            return Data([colorbar, triangles])
        else: 
            return  Data([triangles])
    else:#plot edges
        #define the lists Xe, Ye, Ze, of x, y, resp z coordinates of edge end points for each triangle
        #None separates data corresponding to two consecutive triangles
        Xe=[]
        Ye=[]
        Ze=[]
        for T in tri_vertices:
            Xe+=[T[k%3][0] for k in range(4)]+[ None]
            Ye+=[T[k%3][1] for k in range(4)]+[ None]
            Ze+=[T[k%3][2] for k in range(4)]+[ None]
       
        #define the lines to be plotted
        lines=Scatter3d(x=Xe,
                        y=Ye,
                        z=np.tile(projZ,len(Xe)),
                        mode='lines',
                        line=Line(color= 'rgb(50,50,50)', width=1.5)
               )
        if  showcolorbar is True:
            return Data([colorbar, triangles, lines])
        else: 
            
            return Data([triangles, lines])
