import sys
import vtk
import numpy as np
from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class OpalShapingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Opal Shaping Software')
        self.setGeometry(100, 100, 1000, 600)

        # Widgets for shape selection
        self.shape_label = QLabel('Select Shape:')
        self.shape_combobox = QComboBox()
        self.shape_combobox.addItems(['Rectangle', 'Oval', 'Round'])
        self.shape_combobox.currentIndexChanged.connect(self.updateDimensionFields)

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

        # Widgets for adding cut parameters
        self.angle_label = QLabel('Angle (degrees):')
        self.angle_input = QLineEdit()

        self.position_label = QLabel('Position (mm):')
        self.position_input = QLineEdit()

        self.direction_label = QLabel('Direction:')
        self.direction_combobox = QComboBox()
        self.direction_combobox.addItems(['Up', 'Down'])

        # Button to add cut
        self.add_cut_button = QPushButton('Add Cut')
        self.add_cut_button.setEnabled(False)  # Disabled until model is generated
        self.add_cut_button.clicked.connect(self.addCut)

        # Button to export STL (placeholder)
        self.export_stl_button = QPushButton('Export STL')
        self.export_stl_button.setEnabled(False)  # Disabled until model is generated
        self.export_stl_button.clicked.connect(self.exportSTL)

        # List widget for displaying cuts
        self.cut_list = QListWidget()

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
        shape_layout = QHBoxLayout()
        shape_layout.addWidget(self.shape_label)
        shape_layout.addWidget(self.shape_combobox)

        dimension_layout = QHBoxLayout()
        dimension_layout.addWidget(self.length_label)
        dimension_layout.addWidget(self.length_input)
        dimension_layout.addWidget(self.width_label)
        dimension_layout.addWidget(self.width_input)
        dimension_layout.addWidget(self.height_label)
        dimension_layout.addWidget(self.height_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_model_button)

        cut_param_layout = QVBoxLayout()
        cut_param_layout.addWidget(QLabel('Add Cut Parameters:'))
        cut_param_layout.addWidget(self.angle_label)
        cut_param_layout.addWidget(self.angle_input)
        cut_param_layout.addWidget(self.position_label)
        cut_param_layout.addWidget(self.position_input)
        cut_param_layout.addWidget(self.direction_label)
        cut_param_layout.addWidget(self.direction_combobox)
        cut_param_layout.addWidget(self.add_cut_button)
        cut_param_layout.addWidget(self.export_stl_button)

        left_layout.addLayout(shape_layout)
        left_layout.addLayout(dimension_layout)
        left_layout.addLayout(button_layout)
        left_layout.addLayout(cut_param_layout)
        left_layout.addWidget(self.vtk_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('Cut List:'))
        right_layout.addWidget(self.cut_list)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

    def updateDimensionFields(self, index):
        # Update dimension labels based on selected shape
        shape = self.shape_combobox.currentText()

        if shape == 'Rectangle':
            self.length_label.setText('Length (mm):')
            self.width_label.setText('Width (mm):')
            self.height_label.setText('Height (mm):')
        elif shape == 'Oval':
            self.length_label.setText('Major Axis (mm):')
            self.width_label.setText('Minor Axis (mm):')
            self.height_label.setText('Height (mm):')
        elif shape == 'Round':
            self.length_label.setText('Diameter (mm):')
            self.width_label.setVisible(False)
            self.width_input.setVisible(False)
            self.height_label.setText('Height (mm):')

    def generateModel(self):
        # Implement model generation based on shape and dimensions input using VTK
        shape = self.shape_combobox.currentText()

        try:
            length = float(self.length_input.text())
            width = float(self.width_input.text()) if self.width_input.isVisible() else None
            height = float(self.height_input.text())

            if shape == 'Rectangle':
                self.createRectangle(length, width, height)
            elif shape == 'Oval':
                self.createOval(length, width, height)
            elif shape == 'Round':
                self.createRound(length, height)

            self.add_cut_button.setEnabled(True)
            self.export_stl_button.setEnabled(True)
            self.clearCutList()

        except ValueError:
            print("Invalid input. Please enter numeric values for dimensions.")

    def createRectangle(self, length, width, height):
        # Create a rectangular prism (cube) based on dimensions using VTK
        cube = vtk.vtkCubeSource()
        cube.SetXLength(length)
        cube.SetYLength(width)
        cube.SetZLength(height)

        self.displayModel(cube)

    def createOval(self, major_axis, minor_axis, height):
        # Create an elliptical cylinder (oval) based on dimensions using VTK
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetRadius(major_axis / 2.0)  # Major axis represents diameter in VTK
        cylinder.SetHeight(height)
        cylinder.SetResolution(50)  # Adjust resolution as needed

        transform = vtk.vtkTransform()
        transform.RotateX(90.0)  # Rotate cylinder to align with Z-axis

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputConnection(cylinder.GetOutputPort())
        transform_filter.SetTransform(transform)

        self.displayModel(transform_filter)

    def createRound(self, diameter, height):
        # Create a cylinder (round) based on dimensions using VTK
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetRadius(diameter / 2.0)  # Diameter represents radius in VTK
        cylinder.SetHeight(height)
        cylinder.SetResolution(50)  # Adjust resolution as needed

        self.displayModel(cylinder)

    def displayModel(self, vtk_object):
        # Display the 3D model in the VTK render window
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(vtk_object.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.ren.RemoveAllViewProps()
        self.ren.AddActor(actor)
        self.ren.ResetCamera()

        self.vtk_widget.GetRenderWindow().Render()

    def addCut(self):
        # Add a new cut based on user input
        angle = float(self.angle_input.text())
        position = float(self.position_input.text())
        direction = self.direction_combobox.currentText()

        if direction == 'Up':
            self.executeCut(angle, position, 'above')
        elif direction == 'Down':
            self.executeCut(angle, position, 'below')

        # Add to cut list
        cut_description = f"Angle: {angle}, Position: {position}, Direction: {direction}"
        item = QListWidgetItem(cut_description)
        self.cut_list.addItem(item)

    def executeCut(self, angle, position, direction):
        # Execute cut around the model based on angle, position, and direction
        # Get current model
        actor = self.ren.GetActors().GetLastActor()

        if actor is None:
            print("No model to cut. Generate a model first.")
            return

        polydata = actor.GetMapper().GetInput()

        # Compute slice plane parameters
        normal = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle)), 0.0])
        origin = np.array([0.0, 0.0, position])

        if direction == 'above':
            normal *= -1  # Invert normal direction for above slicing

        # Apply slice operation
        plane = vtk.vtkPlane()
        plane.SetNormal(normal)
        plane.SetOrigin(origin)

        cutter = vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        cutter.SetInputData(polydata)
        cutter.Update()

        # Visualize the sliced model
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(cutter.GetOutput())

        sliced_actor = vtk.vtkActor()
        sliced_actor.SetMapper(mapper)

        self.ren.RemoveAllViewProps()
        self.ren.AddActor(sliced_actor)
        self.ren.ResetCamera()

        self.vtk_widget.GetRenderWindow().Render()

    def clearCutList(self):
        # Clear the cut list widget
        self.cut_list.clear()

    def exportSTL(self):
        # Placeholder for exporting STL functionality
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OpalShapingApp()
    window.show()
    sys.exit(app.exec_())
