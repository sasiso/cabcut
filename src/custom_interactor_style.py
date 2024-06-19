import vtk

class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self):
        self.AddObserver("LeftButtonPressEvent", self.onLeftButtonDown)
        self.AddObserver("LeftButtonReleaseEvent", self.onLeftButtonUp)
        self.AddObserver("MouseMoveEvent", self.onMouseMove)
        self.LeftButtonPressed = False

    def onLeftButtonDown(self, obj, event):
        self.LeftButtonPressed = True

    def onLeftButtonUp(self, obj, event):
        self.LeftButtonPressed = False

    def onMouseMove(self, obj, event):
        # Override the mouse move event to restrict rotation to Z-axis when left button is pressed
        if not self.LeftButtonPressed:
            return

        interactor = self.GetInteractor()
        if interactor is None:
            return

        lastPos = interactor.GetLastEventPosition()
        newPos = interactor.GetEventPosition()

        deltaY = newPos[1] - lastPos[1]

        # Get the active camera associated with the renderer
        renderer = self.GetCurrentRenderer()
        if renderer is None:
            return

        camera = renderer.GetActiveCamera()
        if camera is None:
            return

        # Adjust the camera's azimuth (rotation around Z-axis)
        camera.Azimuth(deltaY)

        # Render the scene
        interactor.Render()
