from typing import List, Union, Literal
from enum import Enum

from pydantic import BaseModel, confloat, conlist


class RobotPosition (BaseModel):
    amcl_positions: conlist(float, min_length=3, max_length=3)
    amcl_orientations: conlist(float, min_length=4, max_length=4)
    odom_pose_positions: conlist(float, min_length=3, max_length=3)
    odom_pose_orientations: conlist(float, min_length=4, max_length=4)
    odom_twist_linear: conlist(float, min_length=3, max_length=3)
    odom_twist_angular: conlist(float, min_length=3, max_length=3)
    path_positions: conlist(List[float], min_length=3, max_length=3)
    path_orientations: conlist(List[float], min_length=4, max_length=4)


class RobotAction(BaseModel):
    action_id: int


class AWCombo(RobotAction):
    name: Literal["awcombo"] = "awcombo"
    x: float = confloat(ge=-5, le=5)
    y: float = confloat(ge=-5, le=5)
    angle: float = confloat(ge=0, le=360)


class Joint(RobotAction):
    name: Literal["joint"] = "joint"
    j1: float = confloat(ge=-1, le=1)
    j2: float = confloat(ge=-1, le=1)
    j3: float = confloat(ge=-1, le=1)
    j4: float = confloat(ge=-1, le=1)
    j5: float = confloat(ge=-1, le=1)
    j6: float = confloat(ge=-1, le=1)


class Carte(RobotAction):
    name: Literal["carte"] = "carte"
    x: float = confloat(ge=-1, le=1)
    y: float = confloat(ge=-1, le=1)
    z: float = confloat(ge=-1, le=1)


class Increm(RobotAction):
    name: Literal["increm"] = "increm"
    axis: Literal["x", "y", "z"]
    delta: float


class SubTask(BaseModel):
    actions: List[Union[Increm, AWCombo, Carte, Joint]]


class RobotActionStatus(Enum):
    RECIEVED = 0
    INPROGRESS = 1
    FINISHED = 2
    FAILED = 3


class RobotActionResponse(BaseModel):
    action_id: int
    status: RobotActionStatus
    log: str
