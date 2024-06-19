import vtk

def createRectangle(length, width, height):
    cube = vtk.vtkCubeSource()
    cube.SetXLength(length)
    cube.SetYLength(height)
    cube.SetZLength(width)
    return cube

def createOval(length, width, height):
    ellipsoid = vtk.vtkSphereSource()
    ellipsoid.SetRadius(1)
    ellipsoid.SetThetaResolution(50)
    ellipsoid.SetPhiResolution(50)

    transform = vtk.vtkTransform()
    transform.Scale(length, height, width)

    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetTransform(transform)
    transform_filter.SetInputConnection(ellipsoid.GetOutputPort())

    return transform_filter

def createRound(length, width, height):
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetRadius(min(length, width) / 2)
    cylinder.SetHeight(height)
    cylinder.SetResolution(50)

    return cylinder

   
