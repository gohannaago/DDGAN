"""
Script to make training dataset for 6*6 
"""
# %%
import os,sys
from numpy.lib.npyio import save
import vtk,vtktools
import u2r
import numpy as np
import matplotlib.pyplot as plt
import random
from nirom_dd_tools import * 
import copy

### MY version of nirom_dd_orig.py for Buildings Case Time Dependent Data

# some functions of tools.io copied in
def write_sing_values(s_values):
    f= open('singular_values.dat',"w+")
    f.write('# index, s_values, normalised s_values, cumulative energy \n' )
    for k in range(len(s_values)):
        #f.write('# field: %s\n' % field[k])
        total = 0.0
        s_values = s_values[k]
        for i in range(len(s_values)):
            total = total + s_values[i]*s_values[i]

        running_total = 0.0
        for i in range(len(s_values)):
            running_total = running_total + s_values[i]*s_values[i]
            f.write ('%d %g %g %18.10g \n' % (i, s_values[i], s_values[i]/s_values[0], running_total/total) )
    f.close()
    return


def get_clean_vtk_file(filename):
    "Removes fields and arrays from a vtk file, leaving the coordinates/connectivity information."
    vtu_data = vtktools.vtu(filename)
    clean_vtu = vtktools.vtu()
    clean_vtu.ugrid.DeepCopy(vtu_data.ugrid)
    fieldNames = clean_vtu.GetFieldNames()
# remove all fields and arrays from this vtu
    for field in fieldNames:
        clean_vtu.RemoveField(field)
        fieldNames = clean_vtu.GetFieldNames()
        vtkdata=clean_vtu.ugrid.GetCellData()
        arrayNames = [vtkdata.GetArrayName(i) for i in range(vtkdata.GetNumberOfArrays())]
    for array in arrayNames:
        vtkdata.RemoveArray(array)
    return clean_vtu

#(nNodes, reconstruction_on_mesh[iTime*nScalar:(iTime+1)*nScalar,:], template_vtu, original_data[0][iTime*nDim:(iTime+1)*nDim], iTime)
def create_vtu_file(path, nNodes, value_mesh_twice_interp, filename, orig_vel, iTime):
    velocity_field = np.zeros((nNodes,3))
    velocity_field[:,0:nDim] = np.transpose(value_mesh_twice_interp[0:nDim,:]) # streamwise component only

    difference = np.zeros((nNodes,3))
    difference[:,0:nDim] = np.transpose(value_mesh_twice_interp[0:nDim,:]) - orig_vel # streamwise component only
    difference = difference / np.max(velocity_field)

    clean_vtk = get_clean_vtk_file(filename)
    new_vtu = vtktools.vtu()
    new_vtu.ugrid.DeepCopy(clean_vtk.ugrid)
    new_vtu.filename = path + 'recon_' + str(iTime) + '.vtu'
    new_vtu.AddField('Velocity',velocity_field)
    new_vtu.AddField('Original',orig_vel)
    new_vtu.AddField('Velocity_diff',difference)
    new_vtu.Write()
    return

def create_vtu_file_timelevel(nNodes, value_mesh_twice_interp, template_vtu, iTime):
    velocity_field = np.zeros((nNodes,3))
    velocity_field[:,0:nDim] = np.transpose(value_mesh_twice_interp[0:nDim,:]) # streamwise component only

#    difference = np.zeros((nNodes,3))
#    difference[:,0:nDim] = np.transpose(value_mesh_twice_interp[0:nDim,:]) - orig_vel # streamwise component only

    clean_vtk = get_clean_vtk_file(template_vtu)
    new_vtu = vtktools.vtu()
    new_vtu.ugrid.DeepCopy(clean_vtk.ugrid)
    new_vtu.filename = 'reconstructed_' + str(iTime) + '.vtu'
    new_vtu.AddField('Velocity',velocity_field)
    #new_vtu.AddField('Velocity_diff',difference)
    new_vtu.Write()
    return

#code for full domain case
# def get_grid_end_points(grid_origin,grid_width,iGrid ):
#     return np.array(( grid_origin[0]+iGrid*grid_width[0], grid_origin[1] +iGrid*grid_width[1]))#

def get_grid_end_points(grid_origin,grid_width):
    return np.array((grid_origin[0]+grid_width[0], grid_origin[1] +grid_width[1]))

def plot_grid(grid_origin, grid_width, nx, ny):
    # include plot of entire coordinates with grid
    plt.figure(figsize=(9,9))
    plt.plot(coordinates[:,0], coordinates[:,1], 'g.', ms = 0.3, label = 'angle = {}˚'.format(rangle)) # corrdinates

    # code for just the edges
    # plt.plot([grid_origin[0], grid_origin[0]+grid_width[0]], [grid_origin[1], grid_origin[1]], 'ko-') #1
    # plt.plot([grid_origin[0], grid_origin[0]], [grid_origin[1], grid_origin[1]+grid_width[1]], 'ko-') #2
    # plt.plot([grid_origin[0], grid_origin[0]+grid_width[0]], [grid_origin[1]+grid_width[1], grid_origin[1]+grid_width[1]], 'ko-') #3
    # plt.plot([grid_origin[0]+grid_width[0], grid_origin[0]+grid_width[0]], [grid_origin[1], grid_origin[1]+grid_width[1]], 'ko-') #4

    for d in range(ny + 1):
        if d%4 == 0:
            plt.plot([grid_origin[0], grid_origin[0]+grid_width[0]], [grid_origin[1]+d*ddx[1], grid_origin[1]+d*ddx[1]], 'k-', lw = 1.2)   #horizontal
            if ny == nx:
                plt.plot([grid_origin[0]+d*ddx[1], grid_origin[0]+d*ddx[1]], [grid_origin[1], grid_origin[1]+grid_width[1]], 'k-', lw = 1.2) #vertical

    if ny != nx:
        for d in range (nx + 1): #vertical
            if d%4 == 0:
                plt.plot([grid_origin[0]+d*ddx[0], grid_origin[0]+d*ddx[0]], [grid_origin[1], grid_origin[1]+grid_width[1]], 'k-', lw = 1.2) #vertical


    plt.grid(':')
    plt.tight_layout()
    plt.legend(loc = 'best')
    # plt.show()

def rotate_mesh(angle):
    theta = np.radians(angle)

    #shift coordinates so that they are centred at (0,0)
    # for i in range(coordinates.shape[0]):
    #     coordinates[i][0] -= 1.5
    #     coordinates[i][1] -= 1.5

    new_mesh = np.zeros(coordinates.shape)

    for i in range(coordinates.shape[0]):
        new_mesh[i][0] = (coordinates[i][0]-(xlength/2))*np.cos(theta) - (coordinates[i][1]-(xlength/2))*np.sin(theta)
        new_mesh[i][1] = (coordinates[i][0]-(xlength/2))*np.sin(theta) + (coordinates[i][1]-(xlength/2))*np.cos(theta)

    #rotate the velocity field as well

    return new_mesh

def rotate_vel(angle, velocity_field):
    theta = np.radians(angle)
    new_mesh = np.zeros(velocity_field.shape)

    for i in range(coordinates.shape[0]):
        new_mesh[i][0] = (velocity_field[i][0])*np.cos(theta) - (velocity_field[i][1])*np.sin(theta)
        new_mesh[i][1] = (velocity_field[i][0])*np.sin(theta) + (velocity_field[i][1])*np.cos(theta)

    return new_mesh

def select_gridpoint():
    min_x = min(coordinates[:,0])
    max_x = max(coordinates[:,0])
    min_y = min(coordinates[:,1])
    max_y = max(coordinates[:,1])

    grid_origin = [9,9]
    while np.sqrt(grid_origin[0]**2+grid_origin[1]**2) >= 2.75:
        # print("finding point - ", np.sqrt(grid_origin[0]**2+grid_origin[1]**2))
        grid_origin = [random.uniform(min_x+0.8, max_x-1.3), random.uniform(min_y+0.8, max_y-1.3)]

    return grid_origin

def sample_starshape(mesh, grid_origin):
    """
    Returns a snapshot matrix of shape (5,nx*ny) and 
    snapshot_ae of shape (5,nx,ny) with given
    mesh and central grid origin for the starshape grid formation
    """
    grid_point_0 = [grid_origin[0], grid_origin[1]+grid_width[1]]
    grid_point_1 = [grid_origin[0]-grid_width[0], grid_origin[1]]
    grid_point_2 = [grid_origin[0]+grid_width[0], grid_origin[1]]
    grid_point_3 = [grid_origin[0], grid_origin[1]-grid_width[1]]
    #grid_point_4 = grid_origin
    
    grid_list = [grid_point_0,grid_point_1, grid_point_2, grid_point_3, grid_origin]

    s_matrix = np.zeros((nx*ny, 5))
    s_ae = np.zeros((5,nx,ny))

    for iloc in range(5):
        value_grid = u2r.simple_interpolate_from_mesh_to_grid(mesh, x_all, x_ndgln, ddx, grid_list[iloc], nx, ny, nz, zeros_beyond_mesh, nEl, nloc, nNodes, nScalar, nDim,1)
        s_matrix[:,iloc] = value_grid.reshape(-1)
        s_ae[iloc,:,:] = value_grid.reshape((nx,ny))

    return s_matrix, s_ae

def plot_starshape(nSGrids, iTime, iField = 0):
    plt.figure(figsize=(8,8))
    plt.subplot(3,3,2)
    plt.imshow(np.rot90(Ssnapshot_ae[iTime,5*nSGrids,:,:,iField]))

    plt.subplot(3,3,4)
    plt.imshow(np.rot90(Ssnapshot_ae[iTime,5*nSGrids+1,:,:,iField]))

    plt.subplot(3,3,5)
    plt.imshow(np.rot90(Ssnapshot_ae[iTime,5*nSGrids+4,:,:,iField]))

    plt.subplot(3,3,6)
    plt.imshow(np.rot90(Ssnapshot_ae[iTime,5*nSGrids+2,:,:,iField]))

    plt.subplot(3,3,8)
    plt.imshow(np.rot90(Ssnapshot_ae[iTime,5*nSGrids+3,:,:,iField]))

    plt.tight_layout()
    # plt.show()


## settings

snapshot_data_location = '../data/'
snapshot_file_base = 'Flow_past_buildings_'

nTime = 475
offset = 25
t_step = 1
field_names = ['Velocity', 'VelocityAbsorption']
nFields = len(field_names)

assert nTime <= (500 - offset), "Time range nTime is larger than what comprises full dataset"

# nSnapshots = nTime // t_step
# print("Number of time level Snapshots = ", nSnapshots)
xlength = 6.0  
ylength = 6.0

grid_width = [0.5,0.5]
# spacing inside small grid 
nx = int(grid_width[0]*100)
ny = nx
nz = 1
ddx = np.array((0.01,0.01))

# set number of grids - samples/snapshots to take
# nGrids = 3000
# Turn on/off snapshots matrix 
save_snapshots = False
save_stargrid = True
# Turn on/off save first 20 images
save_imgs = True

# get a vtu file (any will do as the mesh is not adapted)
filename = snapshot_data_location + snapshot_file_base + '84.vtu'
representative_vtu = vtktools.vtu(filename)
coordinates_org = representative_vtu.GetLocations() #coordinates of the nodes
coordinates = coordinates_org

nNodes = coordinates.shape[0] # vtu_data.ugrid.GetNumberOfPoints()
nEl = representative_vtu.ugrid.GetNumberOfCells()
# print('nEl', nEl, type(nEl), 'nNodes', nNodes) 
#nNodes = 375627
#nEl = 125209
nloc = 3 # number of local nodes, ie three nodes per element (in 2D)
# nScalar = 2 # dimension of fields , 2 = u and v
nScalar = 1 #because I calculate u and v separately
nDim = 2 # dimension of problem (no need to interpolate in the third dimension)

# x_all = np.transpose(coordinates[:,0:nDim]) ### coords n,3  x_all 2,n

# get global node numbers
x_ndgln = np.zeros((nEl*nloc), dtype=int)
for iEl in range(nEl):
    n = representative_vtu.GetCellPoints(iEl) + 1
    x_ndgln[iEl*nloc:(iEl+1)*nloc] = n


# %%

print("Generating starshape grids")
zeros_beyond_mesh = 0

#load central grids and angles
# origin_save = np.load("grid_origins.npy")
# rangle_save = np.load("rotation_angles.npy")

#set number of starshape grids to use
nSGrids = 2000
# print("Number of available central grids: ", len(origin_save))
# assert nSGrids <= nGrids, "Cannot make more starshape grids than number of central grids we have"
# Ssnapshots_matrix = np.zeros((nx*ny*3, nSGrids*5))
Ssnapshot_ae = np.zeros((nSGrids*2*5,nx,ny,3))

for iGrid in range(nSGrids):
    rand_t = random.randint(offset, nTime+offset-1)
    print("Sampling at starshape grid ", iGrid+1, " out of ", nSGrids)

    # call saved values for grid origin and random angle
    # grid_origin = origin_save[iGrid] #have offset of 50
    # rangle = rangle_save[iGrid]

    #find new random location and location
    grid_origin = select_gridpoint()
    rangle = random.randint(0,360)
    # print("grid origin", grid_origin[0], grid_origin[1], ", angle = ", rangle)

    for i in range(2):
        iTime = rand_t+(i*t_step)
        print("Sampling at Timestep ", iTime)
        filename = snapshot_data_location + snapshot_file_base + str(iTime) + '.vtu'
        vtu_data = vtktools.vtu(filename)
        iSnapshot = iTime // t_step

        # print("rangle ", rangle, "grid_origin", grid_origin[0], grid_origin[1])

        coordinates_org = vtu_data.GetLocations() #coordinates of the nodes
        nEl = vtu_data.ugrid.GetNumberOfCells()
        x_ndgln = np.zeros((nEl*nloc), dtype=int)
        for iEl in range(nEl):
            n = vtu_data.GetCellPoints(iEl) + 1
            x_ndgln[iEl*nloc:(iEl+1)*nloc] = n
        # print("nEl for time level ", iTime, " = ", nEl)

        # rotate mesh and velocity
        coordinates = coordinates_org
        coordinates = rotate_mesh(rangle)

        if iGrid <= 50 and i == 0:
            plot_grid(grid_origin, grid_width, nx, ny)
            plt.savefig("imgs/grid_" + str(iGrid) + ".png")
            plt.close()

        nNodes = coordinates.shape[0] # vtu_data.ugrid.GetNumberOfPoints()
        x_all = np.transpose(coordinates[:,0:nDim])
        velocity_field = vtu_data.GetField(field_names[0])[:,:nDim] #field name 0 is velocity field
        velocity_field = rotate_vel(rangle, velocity_field) #rotate velocity
        va_field = vtu_data.GetField(field_names[1])[:,0]

        index = (iGrid*2)+ i
        # print("Snapshot index: ", index)

        #starshape for u_vel
        u_mesh = np.zeros((1,nNodes,1))
        u_mesh[:,:,0] = np.transpose(velocity_field[:,0])
        _, u_sae = sample_starshape(u_mesh, grid_origin)
        # Ssnapshots_matrix[:nx*ny,5*iGrid:5*iGrid+5] = u_smatrix
        Ssnapshot_ae[5*index:5*index+5,:,:,0] = u_sae

        #starshape for v_vel
        v_mesh = np.zeros((1,nNodes,1))
        v_mesh[:,:,0] = np.transpose(velocity_field[:,1])
        _, v_sae = sample_starshape(v_mesh, grid_origin)
        # Ssnapshots_matrix[nx*ny:nx*ny*2,5*iGrid:5*iGrid+5] = v_smatrix
        Ssnapshot_ae[5*index:5*index+5,:,:,1] = v_sae

        #starshape for va
        va_mesh = np.zeros((1,nNodes,1))
        va_mesh[:,:,0] = np.transpose(va_field)
        va_smatrix, va_sae = sample_starshape(va_mesh, grid_origin)
        # Ssnapshots_matrix[nx*ny*2:nx*ny*3,5*iGrid:5*iGrid+5] = va_smatrix
        Ssnapshot_ae[5*index:5*index+5,:,:,2] = va_sae

#Scale values
# min_vel = np.amin(Ssnapshots_matrix[:nx*ny*2,:]) #minimum among u and v velocity
# max_vel = np.amax(Ssnapshots_matrix[:nx*ny*2,:])
min_vel = np.amin(Ssnapshot_ae[:,:,:,:2])
max_vel = np.amax(Ssnapshot_ae[:,:,:,:2])
# min_vel = -6.545574188232422
# max_vel = 6.623080253601074
vel_scaling = 1/(max_vel-min_vel)

min_va = np.amin(Ssnapshot_ae[:,:,:,2])
max_va = np.amax(Ssnapshot_ae[:,:,:,2])
va_scaling = 1/(max_va - min_va)

#scale snapshots for ae
# Ssnapshot_ae = vel_scaling*(Ssnapshot_ae-min_vel)
Ssnapshot_ae[:,:,:,:2] = vel_scaling*(Ssnapshot_ae[:,:,:,:2]-min_vel)
Ssnapshot_ae[:,:,:,2] = va_scaling*Ssnapshot_ae[:,:,:,2]

# print("Scaled minimum = ", np.amin(Ssnapshot_ae[:,:,:,:2]))
# print("Scaled maximum = ", np.amax(Ssnapshot_ae[:,:,:,:2]))

np.save("training_set_8.npy",Ssnapshot_ae)


textfile = open("training_set_8.txt", 'w')
textfile.write("min_vel = "+str(min_vel) +" , max_vel = "+ str(max_vel)+ " , vel_scaling = "+ str(vel_scaling))
textfile.close()

print("min_vel = ", min_vel, " , max_vel = ", max_vel, " , vel_scaling = ", vel_scaling)

# %%
