import functools

import construct
from construct.core import Const, Construct, Enum, Float32l, Hex, Int32sl, Int32ul, Struct

from mercury_engine_data_structures.common_types import CVector2D, CVector3D, StrId, make_vector
from mercury_engine_data_structures.formats import BaseResource
from mercury_engine_data_structures.game_check import Game

TileType = Enum(
    Int32ul,
    NORMAL=1,
    HEAT=2,
    ACID=4,
    ACID_RISE=8,
    ACID_FALL=12
)

IconPriority = Enum(
    Int32sl,
    METROID=-1,
    ACTOR=0,
    ENERGY_CLOUD=2,
    DOOR=3,
    CHOZO_SEAL=4,
    HIDDEN_ITEM=5
)

# BMSMSD
BMSMSD = Struct(
    "_magic" / Const(b"MMSD"),
    "version" / Const(0x00070001, Hex(Int32ul)),
    "scenario" / StrId,
    "tile_size" / construct.Array(2, Float32l),
    "x_tiles" / Int32sl,
    "y_tiles" / Int32sl,
    "map_dimensions" / Struct(
        "bottom_left" / CVector2D,
        "top_right" / CVector2D,
    ),
    "tiles" / make_vector(
        Struct(
            "tile_coordinates" / construct.Array(2, Int32sl),
            "tile_dimension" / Struct(
                "bottom_left" / CVector2D,
                "top_right" / CVector2D,
            ),
            "border_type" / Int32sl,
            "tile_type" / TileType,
            "icons" / make_vector(
                Struct(
                    "actor_name" / StrId,
                    "clear_condition" / StrId,
                    "icon" / StrId,
                    "icon_priority" / IconPriority,
                    "coordinates" / CVector3D,
                )
            ),
        )
    ),
    construct.Terminated,
)


class Bmsmsd(BaseResource):
    @classmethod
    @functools.lru_cache
    def construct_class(cls, target_game: Game) -> Construct:
        return BMSMSD
