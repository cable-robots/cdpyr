import numpy as np
import pytest
import vtk

import cdpyr


def draw_workspace(vertices: np.ndarray, faces: np.ndarray):
    colors = vtk.vtkNamedColors()

    # create polyhedron (cube)
    # The point Ids are: [0, 1, 2, 3, 4, 5, 6, 7]

    points = vtk.vtkPoints()
    for vertex in vertices:
        points.InsertNextPoint(*vertex)

    # These are the point ids corresponding to each face.
    faceId = vtk.vtkIdList()
    faceId.InsertNextId(faces.shape[0])  # Six faces make up the cell.
    for face in faces:
        faceId.InsertNextId(len(face))  # The number of points in the face.
        [faceId.InsertNextId(i) for i in face]

    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(vtk.VTK_POLYHEDRON, faceId)

    # Create a mapper and actor
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(ugrid)

    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetInputData(ugrid)
    writer.SetFileName('polyhedron.vtu')
    writer.SetDataModeToAscii()
    writer.Update()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Silver'))

    # Visualize
    renderer = vtk.vtkRenderer()
    window = vtk.vtkRenderWindow()
    window.SetSize(1600, 1000)
    window.SetWindowName('Polyhedron')
    window.AddRenderer(renderer)
    window_interactor = vtk.vtkRenderWindowInteractor()
    window_interactor.SetRenderWindow(window)

    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('Salmon'))
    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(30)
    renderer.GetActiveCamera().Elevation(30)
    window.Render()
    window_interactor.Start()


class GridWorkspaceTestSuite(object):

    def test_3r3t_ik_standard_translation_cable_length(self,
                                                       robot_3r3t:
                                                       'cdpyr.robot.Robot',
                                                       ik_standard:
                                                       'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criteria and their parameters we want to evaluate
        criteria = [
            (
                cdpyr.analysis.workspace.Criterion.CABLE_LENGTH,
                {
                    'limits': [np.sqrt(0.5 ** 2 + 0.5 ** 2 + 0.5 ** 2),
                               np.sqrt(1.5 ** 2 + 1.5 ** 2 + 1.5 ** 2)],
                }
            )
        ]

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.HULL
        # place center of hull at the world origin
        method.center = [0.0, 0.0, 0.0]

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criteria,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace, faces = workspace_calculator.evaluate(robot_3r3t)

        # get corners of workspace
        corners = np.asarray([p[0] for p in workspace])

        draw_workspace(corners, faces)

        assert False

    def test_3r3t_ik_standard_translation_singularities(self,
                                                        robot_3r3t:
                                                        'cdpyr.robot.Robot',
                                                        ik_standard:
                                                        'cdpyr.analysis.kinematics.Calculator'):
        # workspace archetype we want to calculate
        archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
        archetype.dcm = np.eye(3)

        # criteria and their parameters we want to evaluate
        criteria = [
            (
                cdpyr.analysis.workspace.Criterion.SINGULARITIES
            )
        ]

        # method we want to use to calculate the workspace
        method = cdpyr.analysis.workspace.Method.HULL
        # place center of hull at the world origin
        method.center = [0.0, 0.0, 0.0]

        # a workspace calculator object
        workspace_calculator = cdpyr.analysis.workspace.Calculator(
            archetype,
            method,
            criteria,
            kinematics=ik_standard)

        # evaluate the workspace over the grid
        workspace, faces = workspace_calculator.evaluate(robot_3r3t)

        # get corners of workspace
        corners = np.asarray([p[0] for p in workspace])

        draw_workspace(corners, faces)

        assert False

    # def test_3r3t_ik_standard_translation_wrench_feasible(self,
    #                                                       robot_3r3t:
    #                                                       'cdpyr.robot.Robot',
    #                                                       ik_standard:
    #                                                       'cdpyr.analysis.kinematics.Calculator'):
    #     # workspace archetype we want to calculate
    #     archetype = cdpyr.analysis.workspace.Archetype.TRANSLATION
    #     archetype.dcm = np.eye(3)
    #
    #     # criteria and their parameters we want to evaluate
    #     criteria = [
    #         (
    #             cdpyr.analysis.workspace.Criterion.WRENCH_FEASIBLE,
    #             {
    #                 'wrench':    [0.0, 0.0, -9.81, 0.0, 0.0, 0.0],
    #                 'force_min': 1,
    #                 'force_max': 10,
    #             }
    #         )
    #     ]
    #
    #     # method we want to use to calculate the workspace
    #     method = cdpyr.analysis.workspace.Method.HULL
    #     # place center of hull at the world origin
    #     method.center = [0.0, 0.0, 0.0]
    #
    #     # a workspace calculator object
    #     workspace_calculator = cdpyr.analysis.workspace.Calculator(
    #         archetype,
    #         method,
    #         criteria,
    #         kinematics=ik_standard)
    #
    #     # evaluate the workspace over the grid
    #     workspace, faces = workspace_calculator.evaluate(robot_3r3t)
    #
    #     # get corners of workspace
    #     corners = np.asarray([p[0] for p in workspace])
    #
    #     draw_workspace(corners, faces)
    #
    #     assert False


if __name__ == "__main__":
    pytest.main()
