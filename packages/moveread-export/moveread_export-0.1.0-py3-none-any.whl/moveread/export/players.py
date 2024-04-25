import asyncio
from kv.api import KV
from haskellian import Either, Left, IsLeft, Right, iter as I
from cv2 import Mat
from moveread.core import Player
from moveread.labels import export, ChessError
from .sheets import sheet_boxes

async def player_boxes(player: Player, *, blobs: KV[bytes]) -> list[list[Mat]]:
  """Returns ply-major boxes (`result[ply][img_version]`)"""
  boxes = await asyncio.gather(*[sheet_boxes(sheet, blobs=blobs) for sheet in player.sheets])
  return list(I.flatten(boxes))

def player_labels(player: Player, pgn: list[str]) -> Either[ChessError, list[str]]:
  return Right(pgn) if player.meta is None else export(pgn, player.meta)

async def player_samples(player: Player, pgn: list[str], *, blobs: KV[bytes]) -> Either[ChessError, list[list[tuple[Mat, str]]]]:
  """Returns ply-major samples (`result[ply][img_version]`)"""
  try:
    labels = player_labels(player, pgn).unsafe()
    boxes = await player_boxes(player, blobs=blobs)
    return Right([
      [(b, lab) for b in bxs]
      for bxs, lab in zip(boxes, labels)
    ])
  except IsLeft as e:
    return Left(e.value)