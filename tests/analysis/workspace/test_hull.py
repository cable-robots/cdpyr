import sys

import numpy as np
import pytest
import vtk

from cdpyr.analysis import force_distribution, workspace
from cdpyr.analysis.kinematics.algorithm import Algorithm as Kinematics
from cdpyr.robot import Robot


def plot_workspace(ws: workspace.HULL_RESULT, title):
    return

    colors = vtk.vtkNamedColors()

    points = vtk.vtkPoints()
    for vertex in ws.vertices:
        points.InsertNextPoint(*vertex)

    # These are the point ids corresponding to each face.
    faceId = vtk.vtkIdList()
    faceId.InsertNextId(ws.faces.shape[0])  # Six faces make up the cell.
    for face in ws.faces:
        faceId.InsertNextId(len(face))  # The number of points in the face.
        [faceId.InsertNextId(i) for i in face]

    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(vtk.VTK_POLYHEDRON, faceId)

    # Create a mapper and actor
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(ugrid)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Silver'))

    # Visualize
    renderer = vtk.vtkRenderer()
    window = vtk.vtkRenderWindow()
    window.SetSize(1600, 1000)
    window.SetWindowName(title)
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


class HullWorkspaceTestSuite(object):

    # def test_1t_ik_standard_translation_cable_length(self,
    #                                                  robot_1t: Robot,
    #                                                  ik_standard: Kinematics):
    #     # workspace archetype we want to calculate
    #     archetype = workspace.archetype.TRANSLATION(
    #         dcm=np.eye(3)
    #     )
    #
    #     # criterion and its parameters we want to evaluate
    #     criterion = workspace.criterion.CABLE_LENGTH(
    #         kinematics=ik_standard,
    #         limits=[0.5, 1.5]
    #     )
    #
    #     # method we want to use to calculate the workspace
    #     method = workspace.HULL(
    #         ik_standard,
    #         archetype,
    #         criterion,
    #         # place center of hull at the world origin
    #         center=0.0
    #     )
    #
    #     # evaluate the workspace over the grid
    #     ws = method.evaluate(robot_1t)
    #
    #     plot_workspace(ws, sys._getframe().f_code.co_name)
    #
    #     assert False

    # def test_1t_ik_standard_translation_singularities(self,
    #                                                   robot_1t: Robot,
    #                                                   ik_standard:
    #                                                   Kinematics):
    #     # workspace archetype we want to calculate
    #     archetype = workspace.archetype.TRANSLATION(
    #         dcm=np.eye(3)
    #     )
    #
    #     # criteria and their parameters we want to evaluate
    #     criterion = workspace.criterion.SINGULARITIES(
    #         kinematics=ik_standard
    #     )
    #
    #     # method we want to use to calculate the workspace
    #     method = workspace.HULL(
    #         ik_standard,
    #         archetype,
    #         criterion,
    #         # place center of hull at the world origin
    #         center=0.0
    #     )
    #
    #     # evaluate the workspace over the grid
    #     ws = method.evaluate(robot_1t)
    #
    #     plot_workspace(ws, sys._getframe().f_code.co_name)
    #
    #     assert False

    # def test_1t_ik_standard_translation_wrench_closure(self,
    #                                                    robot_1t: Robot,
    #                                                    ik_standard:
    #                                                    Kinematics):
    #     # workspace archetype we want to calculate
    #     archetype = workspace.archetype.TRANSLATION(
    #         dcm=np.eye(3)
    #     )
    #
    #     # criterion and their parameters we want to evaluate
    #     criterion = workspace.criterion.WRENCH_CLOSURE(
    #         force_distribution=force_distribution.CLOSED_FORM(
    #             ik_standard,
    #             force_minimum=[1],
    #             force_maximum=[10],
    #         ),
    #         wrench=-1
    #     )
    #
    #     # method we want to use to calculate the workspace
    #     method = workspace.HULL(
    #         ik_standard,
    #         archetype,
    #         criterion,
    #         # place center of hull at the world origin
    #         center=0.0
    #     )
    #
    #     # evaluate the workspace over the grid
    #     ws = method.evaluate(robot_1t)
    #
    #     plot_workspace(ws, sys._getframe().f_code.co_name)
    #
    #     assert False

    # def test_1t_ik_standard_translation_wrench_feasible(self,
    #                                                     robot_1t: Robot,
    #                                                     ik_standard:
    #                                                     Kinematics):
    #     # workspace archetype we want to calculate
    #     archetype = workspace.archetype.TRANSLATION(
    #         dcm=np.eye(3)
    #     )
    #
    #     # criterion and their parameters we want to evaluate
    #     criterion = workspace.criterion.WRENCH_FEASIBLE(
    #         force_distribution=force_distribution.CLOSED_FORM(
    #             ik_standard,
    #             force_minimum=[0],
    #             force_maximum=[np.inf]
    #         ),
    #         wrench=-1
    #     )
    #
    #     # method we want to use to calculate the workspace
    #     method = workspace.HULL(
    #         ik_standard,
    #         archetype,
    #         criterion,
    #         # place center of hull at the world origin
    #         center=0.0
    #     )
    #
    #     # evaluate the workspace over the grid
    #     ws = method.evaluate(robot_1t)
    #
    #     plot_workspace(ws, sys._getframe().f_code.co_name)
    #
    #     assert False

    def test_3r3t_ik_standard_translation_cable_length(self,
                                                       robot_3r3t: Robot,
                                                       ik_standard:
                                                       Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and its parameters we want to evaluate
        criterion = workspace.criterion.CABLE_LENGTH(
            kinematics=ik_standard,
            limits=[0.866025404, 2.598076211]
        )

        # method we want to use to calculate the workspace
        method = workspace.HULL(
            ik_standard,
            archetype,
            criterion,
            # place center of hull at the world origin
            center=[0.0, 0.0, 0.0]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(ws, sys._getframe().f_code.co_name)

        assert ws.surface > 0
        assert ws.volume > 0
        assert [0.0, 0.0, 0.0] in ws
        assert [0.5, 0.5, 0.5] not in ws
        assert [1.0, 1.0, 1.0] not in ws


    def test_3r3t_ik_standard_translation_wrench_closure(self,
                                                         robot_3r3t: Robot,
                                                         ik_standard:
                                                         Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and their parameters we want to evaluate
        criterion = workspace.criterion.WRENCH_CLOSURE(
            force_distribution=force_distribution.CLOSED_FORM(
                ik_standard,
                force_minimum=[1],
                force_maximum=[10]
            ),
            wrench=[0.0, 0.0, -9.81, 0.0, 0.0, 0.0]
        )

        # method we want to use to calculate the workspace
        method = workspace.HULL(
            ik_standard,
            archetype,
            criterion,
            # place center of hull at the world origin
            center=[0.0, 0.0, 0.0]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(ws, sys._getframe().f_code.co_name)

        assert ws.surface > 0
        assert ws.volume > 0
        assert [0.0, 0.0, 0.0] in ws
        assert [0.5, 0.5, 0.5] in ws
        assert [1.0, 1.0, 1.0] in ws


    def test_3r3t_ik_standard_translation_wrench_feasible(self,
                                                          robot_3r3t: Robot,
                                                          ik_standard:
                                                          Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criterion and their parameters we want to evaluate
        criterion = workspace.criterion.WRENCH_FEASIBLE(
            force_distribution=force_distribution.CLOSED_FORM(
                ik_standard,
                force_minimum=[0],
                force_maximum=[np.inf]
            ),
            wrench=[0.0, 0.0, -9.81, 0.0, 0.0, 0.0]
        )

        # method we want to use to calculate the workspace
        method = workspace.HULL(
            ik_standard,
            archetype,
            criterion,
            # place center of hull at the world origin
            center=[0.0, 0.0, 0.0]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(ws, sys._getframe().f_code.co_name)

        assert ws.surface > 0
        assert ws.volume > 0
        assert [0.0, 0.0, 0.0] in ws
        assert [0.5, 0.5, 0.5] in ws
        assert [1.0, 1.0, 1.0] in ws


    def test_3r3t_ik_standard_translation_singularities(self,
                                                        robot_3r3t: Robot,
                                                        ik_standard:
                                                        Kinematics):
        # workspace archetype we want to calculate
        archetype = workspace.archetype.TRANSLATION(
            dcm=np.eye(3)
        )

        # criteria and their parameters we want to evaluate
        criterion = workspace.criterion.SINGULARITIES(
            kinematics=ik_standard
        )

        # method we want to use to calculate the workspace
        method = workspace.HULL(
            ik_standard,
            archetype,
            criterion,
            # place center of hull at the world origin
            center=[0.0, 0.0, 0.0]
        )

        # evaluate the workspace over the grid
        ws = method.evaluate(robot_3r3t)

        plot_workspace(ws, sys._getframe().f_code.co_name)

        assert ws.surface == 0
        assert ws.volume == 0
        assert [0.0, 0.0, 0.0] not in ws
        assert [0.5, 0.5, 0.5] not in ws
        assert [1.0, 1.0, 1.0] not in ws


if __name__ == "__main__":
    pytest.main()
