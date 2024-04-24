import sys
import warnings
from typing import List, Tuple
from pathlib import Path

import numpy as np
import quaternion
import pyassimp
from pyassimp.structs import Node
from pyassimp.postprocess import aiProcess_Triangulate, aiProcess_MakeLeftHanded

from skanym.loaders.iFileLoader import IFileLoader
from skanym.structures.character.skeleton import Skeleton
from skanym.structures.character.joint import Joint
from skanym.structures.animation.animation import Animation
from skanym.structures.animation.animationCurve import AnimationCurve
from skanym.structures.animation.positionCurve import PositionCurve
from skanym.structures.animation.quaternionCurve import QuaternionCurve
from skanym.structures.animation.key import Key
from skanym.structures.data.transform import Transform
from skanym.utils import conversion


class AssimpLoader(IFileLoader):
    def __init__(self, path: Path):
        super().__init__(path)
        self.joints = None

    def load_skeleton(self) -> Skeleton:
        with pyassimp.load(
            self._path,
            processing=(pyassimp.postprocess.aiProcess_Triangulate),
        ) as scene:
            if scene is None:
                raise Exception(f"Failed to load file: {self._path}")

            allNodeList = self._all_nodes_dfs(scene.rootnode)

            self.joints = self._create_joint_list(allNodeList)

            jointNodeList = self._joint_nodes_dfs(scene.rootnode)

            return self._build_skeleton(jointNodeList)

    def load_animation(self) -> Animation:
        with pyassimp.load(
            self._path,
            processing=(pyassimp.postprocess.aiProcess_Triangulate),
        ) as scene:
            if self.joints is None:
                self.load_skeleton()

            if scene is None:
                raise Exception(f"Failed to load file: {self._path}")

            raw_duration = scene.animations[0].duration
            duration = raw_duration / scene.animations[0].tickspersecond
            animation = Animation(name=scene.animations[0].name, duration=duration)

            animChannels = scene.animations[0].channels
            for channel in animChannels:
                joint_id = self._get_joint_id(
                    channel.nodename.data.decode("utf-8"), self.joints
                )
                current_pos_curve = PositionCurve()
                current_rot_curve = QuaternionCurve()
                if joint_id == 0:
                    for pos_key in channel.positionkeys:
                        current_pos_curve.add_key(
                            Key(
                                time=pos_key.time / raw_duration,
                                value=np.array(
                                    [
                                        pos_key.value[0],
                                        pos_key.value[1],
                                        pos_key.value[2],
                                    ]
                                ),
                            )
                        )

                    animation.position_curves.append(
                        AnimationCurve(curve=current_pos_curve, id=joint_id)
                    )

                for rot_key in channel.rotationkeys:
                    q = np.quaternion(
                        rot_key.value[0],
                        rot_key.value[1],
                        rot_key.value[2],
                        rot_key.value[3],
                    )
                    bind_m = self.joints[joint_id].local_bind_transform.getTransformMatrix()     
                    m_rot = conversion.quaternionToRotationMatrix(q)
                    m = np.identity(4)
                    m[0:3, 0:3] = m_rot
                    delta_m = np.matmul(np.linalg.inv(bind_m), m)
                    delta_q = conversion.rotationMatrixToQuaternion(delta_m[0:3, 0:3])[0]

                    # if delta_q.w < 0:
                    #     delta_q = -delta_q
                    
                    current_rot_curve.add_key(
                        Key(
                            time=rot_key.time / raw_duration,
                            value=quaternion.as_float_array(delta_q),
                        )
                    )

                animation.rotation_curves.append(
                    AnimationCurve(curve=current_rot_curve, id=joint_id)
                )

            for joint_id in range(len(self.joints)):
                if joint_id not in [
                    anim_curve.id for anim_curve in animation.position_curves
                ]:
                    animation.position_curves.append(
                        AnimationCurve(curve=PositionCurve(), id=joint_id)
                    )
                if joint_id not in [
                    anim_curve.id for anim_curve in animation.rotation_curves
                ]:
                    animation.rotation_curves.append(
                        AnimationCurve(curve=QuaternionCurve(), id=joint_id)
                    )

            animation.position_curves.sort(key=lambda x: x.id)
            animation.rotation_curves.sort(key=lambda x: x.id)

            return animation

    def _get_joint(self, name: str, joints: List[Joint]) -> Joint:
        for joint in joints:
            if joint.name == name:
                return joint
        return None

    def _get_joint_id(self, name: str, joints: List[Joint]) -> int:
        for i, joint in enumerate(joints):
            if joint.name == name:
                return i
        return -1

    def _is_joint_node(self, node: Node) -> bool:
        return not ("Translation" in node.name or "Rotation" in node.name)

    def _all_nodes_dfs(self, node: Node, allNodeList: List[Node] = []) -> List[Node]:
        for child in node.children:
            allNodeList.append(child)
            self._all_nodes_dfs(child, allNodeList)
        return allNodeList

    def _joint_nodes_dfs(
        self, node: Node, depth: int = 0, jointNodeList: List[Tuple[str, int]] = []
    ) -> List[Tuple[str, int]]:
        for child in node.children:
            if self._is_joint_node(child):
                jointNodeList.append((child.name, depth))
                depth += 1
            self._joint_nodes_dfs(child, depth, jointNodeList)
        return jointNodeList

    def _create_joint_list(self, allNodeList: List[Node]) -> List[Joint]:
        joints = []
        current_joint = None
        for node in allNodeList[::-1]:
            if not self._is_joint_node(node):
                if "Translation" in node.name:
                    current_joint.local_bind_transform.position = np.array(
                        [
                            node.transformation[0][3],
                            node.transformation[1][3],
                            node.transformation[2][3],
                        ]
                    )
                elif "Rotation" in node.name:
                    rm = (
                        np.array(
                            [
                                node.transformation[0][0],
                                node.transformation[1][0],
                                node.transformation[2][0],
                                node.transformation[0][1],
                                node.transformation[1][1],
                                node.transformation[2][1],
                                node.transformation[0][2],
                                node.transformation[1][2],
                                node.transformation[2][2],
                            ]
                        )
                        .reshape(3, 3)
                        .T
                    )
                    q = conversion.rotationMatrixToQuaternion(rm)[0]
                    current_joint.local_bind_transform.rotation = q

            else:
                current_pos = np.array(
                    [
                        node.transformation[0][3],
                        node.transformation[1][3],
                        node.transformation[2][3],
                    ]
                )
                current_rot = (
                    np.array(
                        [
                            node.transformation[0][0],
                            node.transformation[1][0],
                            node.transformation[2][0],
                            node.transformation[0][1],
                            node.transformation[1][1],
                            node.transformation[2][1],
                            node.transformation[0][2],
                            node.transformation[1][2],
                            node.transformation[2][2],
                        ]
                    )
                    .reshape(3, 3)
                    .T
                )
                q = conversion.rotationMatrixToQuaternion(current_rot)[0]
                # q.z = -q.z
                current_rotation = q

                current_joint = Joint(
                    node.name,
                    local_bind_transform=Transform(
                        position=current_pos, rotation=current_rotation
                    ),
                )
                joints.append(current_joint)

        joints.reverse()
        joints[0].local_bind_transform = Transform()
        return joints

    def _build_skeleton(self, jointNodeList: List[Tuple[str, int]]) -> Skeleton:
        root = None
        parent_stack = []

        for name, depth in jointNodeList:
            current_joint = self._get_joint(name, self.joints)

            if depth == 0:
                root = current_joint
                parent_stack = [root]
            else:
                while len(parent_stack) > depth:
                    parent_stack.pop()
                parent_stack[-1].add_child(current_joint)
                parent_stack.append(current_joint)

        return Skeleton(root)

    def load_animations(self) -> List[Animation]:
        return NotImplementedError


if __name__ == "__main__":
    np.set_printoptions(precision=6, suppress=True)    
    np.set_printoptions(formatter={'float': lambda x: "{: 0.6f}".format(x)})
    file_path = "C:/dev/MotionMachine/3D Animation DB/synthetic-animation-data/animations/run_kh0_sp0_as30.fbx"
    loaderito = AssimpLoader(file_path)
    s = loaderito.load_skeleton()
    a = loaderito.load_animation()
    for anim_curve in a.rotation_curves:
        print(s.get_joint_by_id(anim_curve.id).name)   
        for key in anim_curve.curve.keys[0:3]:
            # if a value is close to 0, set it to 0
            key.value = np.where(np.abs(key.value) < 1e-3, 0, key.value)
            print(key.value)
