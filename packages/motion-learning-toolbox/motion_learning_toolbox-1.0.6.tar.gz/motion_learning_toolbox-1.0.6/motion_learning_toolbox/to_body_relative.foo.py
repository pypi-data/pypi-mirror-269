from typing import Dict, List
from scipy.spatial.transform import Rotation as R
import numpy as np
import pandas as pd


def to_body_relative(
    frames: pd.DataFrame,
    target_joints: List[str],
    coordinate_system: Dict[str, str],
    reference_joint="head",
):
    """
    Transforms position and rotation data into a body-relative coordinate system.

    :param frames: A DataFrame or Series containing position and/or rotation data.
    :param target_joints: A list of joints to be transformed.
    :param coordinate_system: A dictionary specifying the coordinate system for the transformation.
    :param reference_joint: The reference joint used as the origin of the body-relative coordinate system (default is "head").
    """
    reference_pos_columns = [f"{reference_joint}_pos_{xyz}" for xyz in "xyz"]
    target_dtype = frames[reference_pos_columns[0]].to_numpy().dtype
    target_dtype = target_dtype if np.issubdtype(target_dtype, np.floating) else "float32"
    min_float32_dtype = "float32" if target_dtype == np.float16 else target_dtype

    FORWARD = "xyz".index(coordinate_system["forward"])
    RIGHT = "xyz".index(coordinate_system["right"])
    UP = "xyz".index(coordinate_system["up"])
    FORWARD_DIRECTION = np.identity(3, dtype=target_dtype)[FORWARD]
    num_samples = len(frames)

    assert FORWARD != RIGHT != UP
    ## parse rotations of the reference joint (the head)
    reference_rotation_names = [f"{reference_joint}_rot_{c}" for c in "xyzw"]
    reference_rotations = R.from_quat(frames[reference_rotation_names])

    reference_rotation_matrix = reference_rotations.as_matrix()

    f_xz = reference_rotation_matrix[:, :, 2].copy()
    f_xz[:, UP] = 0
    norms = np.linalg.norm(f_xz, axis=1, keepdims=True)
    f_xz_normalized = f_xz / norms

    cos_angles = np.dot(f_xz_normalized, FORWARD_DIRECTION)
    angles = np.arccos(cos_angles)

    # Use the cross product to determine the direction of rotation
    cross_prod = np.cross(f_xz_normalized, FORWARD_DIRECTION)
    angles *= -np.sign(cross_prod[:, 1])
    #
    # hmd_inv_yaw_rotation = R.from_matrix(rot_matrices).inv()
    rotvec = np.zeros((num_samples, 3))
    rotvec[:, 1] = angles
    hmd_inv_yaw_rotation = R.from_rotvec(rotvec).inv()
    # r11 = reference_rotation_matrix[:, 0, 0]
    # r31 = reference_rotation_matrix[:, 2, 0]

    # # Calculate the yaw (rotation around the y-axis)
    # reference_yaw = R.from_euler("y", np.arctan2(r31, r11))

    # hmd_inv_yaw_rotation = reference_yaw.inv()

    ## apply correction positions and rotations
    relative_positions_and_rotations = pd.DataFrame()

    for joint_name in target_joints:  # => joint_name is either `right_hand` or `left_hand`
        # apply rotations to position vector of `joint_name`
        joint_position_names = [f"{joint_name}_pos_{c}" for c in "xyz"]

        relative_position = frames[joint_position_names].values - frames[reference_pos_columns].values

        relative_positions_and_rotations[joint_position_names] = hmd_inv_yaw_rotation.apply(relative_position)

        # rotate the world rotation of `joint_name` by the correction rotation and save quaternion representations
        joint_rotation_names = [f"{joint_name}_rot_{c}" for c in "xyzw"]

        sr_rotations = R.from_quat(frames[joint_rotation_names])
        br_rotations = sr_rotations * hmd_inv_yaw_rotation

        relative_positions_and_rotations[joint_rotation_names] = br_rotations.as_quat().astype(target_dtype)

    # add horizontal rotations of reference joint
    relative_positions_and_rotations[reference_rotation_names] = (reference_rotations * hmd_inv_yaw_rotation).as_quat().astype(target_dtype)

    return relative_positions_and_rotations
