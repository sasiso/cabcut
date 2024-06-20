import vtk
import math

def createRectangle(length, width, height):
    # Create a cube (rectangle)
    cube = vtk.vtkCubeSource()
    cube.SetXLength(length)
    cube.SetYLength(height)
    cube.SetZLength(width)
    cube.Update()
    return cube

def createPerimeterLineAtYPoint(cube, y_point):
    # Get the bounds of the cube
    bounds = cube.GetOutput().GetBounds()
    
    # Create points for the polyline around the object
    points = vtk.vtkPoints()
    points.InsertNextPoint(bounds[0], y_point, bounds[4])
    points.InsertNextPoint(bounds[1], y_point, bounds[4])
    points.InsertNextPoint(bounds[1], y_point, bounds[5])
    points.InsertNextPoint(bounds[0], y_point, bounds[5])
    points.InsertNextPoint(bounds[0], y_point, bounds[4])  # Close the loop
    
    # Create the polyline
    polyline = vtk.vtkPolyLine()
    polyline.GetPointIds().SetNumberOfIds(5)  # Adjust number of points
    for i in range(5):
        polyline.GetPointIds().SetId(i, i)
    
    # Create a cell array to store the lines in and add the lines to it
    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polyline)
    
    # Create a polydata to store everything in
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetLines(cells)
    
    return polyData
    

def createCircleOnTopSurface(cube):
    # Get the bounds of the cube
    bounds = cube.GetOutput().GetBounds()
    
    # Calculate the middle point of the top surface of the cube
    top_center_x = (bounds[0] + bounds[1]) / 2.0
    top_center_y = bounds[3]  # Top surface Y coordinate
    top_center_z = (bounds[4] + bounds[5]) / 2.0
    
    # Create points for the circle (assuming 1 mm radius)
    num_points = 30  # Number of points to create a circle
    points = vtk.vtkPoints()
    for i in range(num_points):
        angle = 2.0 * math.pi * i / num_points
        x = top_center_x + 1.0 * math.cos(angle)
        z = top_center_z + 1.0 * math.sin(angle)
        points.InsertNextPoint(x, top_center_y, z)
    
    # Create polygonal data (closed loop)
    polygon = vtk.vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(num_points)
    for i in range(num_points):
        polygon.GetPointIds().SetId(i, i)
    
    polygons = vtk.vtkCellArray()
    polygons.InsertNextCell(polygon)
    
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetPolys(polygons)
    
    return polyData

def main():
    # Create cube
    cube = createRectangle(50, 30, 20)
    
    # Example Y location for perimeter line
    y_location = 0
    
    # Create renderer and window
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    
    # Create cube actor
    cube_mapper = vtk.vtkPolyDataMapper()
    cube_mapper.SetInputConnection(cube.GetOutputPort())
    cube_actor = vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)
    cube_actor.GetProperty().SetOpacity(0.8)  # 20% transparent
    renderer.AddActor(cube_actor)
    
    # Create perimeter line actor
    perimeter_line = createPerimeterLineAtYPoint(cube, y_location)
    line_mapper = vtk.vtkPolyDataMapper()
    line_mapper.SetInputData(perimeter_line)
    line_actor = vtk.vtkActor()
    line_actor.SetMapper(line_mapper)
    line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Red color for perimeter line
    renderer.AddActor(line_actor)
    
    # Create circle on top surface actor
    circle_polydata = createCircleOnTopSurface(cube)
    circle_mapper = vtk.vtkPolyDataMapper()
    circle_mapper.SetInputData(circle_polydata)
    circle_actor = vtk.vtkActor()
    circle_actor.SetMapper(circle_mapper)
    circle_actor.GetProperty().SetColor(0.0, 0.0, 1.0)  # Blue color for circle
    renderer.AddActor(circle_actor)
    
    # Set up camera and render window parameters
    renderer.ResetCamera()
    render_window.SetSize(600, 600)
    
    # Start interaction
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    main()
