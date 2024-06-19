import sys
import vtk
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QSlider
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from actors import createRectangle, createOval, createRound
from cutting_plane import getCuttingPlaneActor

class OpalShapingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Opal Shaping Software')
        self.setGeometry(100, 100, 1200, 800)

        # Widgets for shape selection
        self.shape_label = QLabel('Select Shape:')
        self.shape_combobox = QComboBox()
        self.shape_combobox.addItems(['Rectangle', 'Oval', 'Round'])

        # Widgets for dimensions input
        self.length_label = QLabel('Length (mm):')
        self.length_input = QLineEdit()

        self.width_label = QLabel('Width (mm):')
        self.width_input = QLineEdit()

        self.height_label = QLabel('Height (mm):')
        self.height_input = QLineEdit()

        # Button to generate initial 3D model
        self.generate_model_button = QPushButton('Generate Model')
        self.generate_model_button.clicked.connect(self.generateModel)

        # Slider for rotating cutting plane
        self.rotation_label = QLabel('Rotation Angle:')
        self.rotation_slider = QSlider()
        self.rotation_slider.setOrientation(PyQt5.QtCore.Qt.Horizontal)
        self.rotation_slider.setMinimum(-180)
        self.rotation_slider.setMaximum(180)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self.rotateCuttingPlane)

        # VTK widget for 3D visualization
        self.vtk_widget = QVTKRenderWindowInteractor()
        self.ren = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.ren)

        # Layout setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.vtk_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.shape_label)
        right_layout.addWidget(self.shape_combobox)
        right_layout.addWidget(self.length_label)
        right_layout.addWidget(self.length_input)
        right_layout.addWidget(self.width_label)
        right_layout.addWidget(self.width_input)
        right_layout.addWidget(self.height_label)
        right_layout.addWidget(self.height_input)
        right_layout.addWidget(self.generate_model_button)
        right_layout.addWidget(self.rotation_label)
        right_layout.addWidget(self.rotation_slider)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        # Add initial cutting plane and axes
        self.addCuttingPlane()

        # Initialize the render window
        self.vtk_widget.Initialize()
        self.vtk_widget.Start()

    def generateModel(self):
        # Generate the initial 3D model based on user input dimensions using VTK
        try:
            shape = self.shape_combobox.currentText()
            length = float(self.length_input.text())
            width = float(self.width_input.text())
            height = float(self.height_input.text())

            if shape == 'Rectangle':
                vtk_object = createRectangle(length, width, height)
            elif shape == 'Oval':
                vtk_object = createOval(length, width, height)
            elif shape == 'Round':
                vtk_object = createRound(length, width, height)

            self.displayModel(vtk_object)
            self.addCuttingPlane()

        except ValueError:
            print("Invalid input. Please enter numeric values for dimensions.")

    def displayModel(self, vtk_object):
        # Display the 3D model in the VTK render window
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(vtk_object.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.ren.RemoveAllViewProps()
        self.ren.AddActor(actor)
        self.addAxes(actor)  # Add axes after adding the actor
        self.ren.ResetCamera()

        self.vtk_widget.GetRenderWindow().Render()

    def addAxes(self, actor):
        # Add X, Y, Z axes to the renderer using vtkCubeAxesActor
        bounds = actor.GetBounds()

        axes = vtk.vtkCubeAxesActor()
        axes.SetBounds(bounds)
        axes.SetCamera(self.ren.GetActiveCamera())
        axes.GetTitleTextProperty(0).SetColor(1, 0, 0)
        axes.GetTitleTextProperty(1).SetColor(0, 1, 0)
        axes.GetTitleTextProperty(2).SetColor(0, 0, 1)
        axes.GetLabelTextProperty(0).SetColor(1, 0, 0)
        axes.GetLabelTextProperty(1).SetColor(0, 1, 0)
        axes.GetLabelTextProperty(2).SetColor(0, 0, 1)

        self.ren.AddActor(axes)
        self.vtk_widget.GetRenderWindow().Render()

    def addCuttingPlane(self):
        # Add cutting plane actor
        self.plane_actor = getCuttingPlaneActor()  # Assuming getCuttingPlaneActor returns a vtkActor
        self.ren.AddActor(self.plane_actor)

    def rotateCuttingPlane(self):
        # Rotate cutting plane based on slider value
        angle = self.rotation_slider.value()
        transform = vtk.vtkTransform()
        transform.RotateWXYZ(angle, 0, 0, 1)
        self.plane_actor.SetUserTransform(transform)
        self.vtk_widget.GetRenderWindow().Render()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OpalShapingApp()
    window.show()
    sys.exit(app.exec_())
