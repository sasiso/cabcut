import vtk

def createCuttingPlane(height=50, width=20, thickness=1):
    plane = vtk.vtkCubeSource()
    plane.SetXLength(thickness)
    plane.SetYLength(height)
    plane.SetZLength(width)
    return plane

def getCuttingPlaneActor():
    plane_source = createCuttingPlane()
    plane_mapper = vtk.vtkPolyDataMapper()
    plane_mapper.SetInputConnection(plane_source.GetOutputPort())

    plane_actor = vtk.vtkActor()
    plane_actor.SetMapper(plane_mapper)
    plane_actor.GetProperty().SetColor(1, 1, 0)  # Yellow color
    plane_actor.GetProperty().SetOpacity(0.5)  # Semi-transparent

    return plane_actor
