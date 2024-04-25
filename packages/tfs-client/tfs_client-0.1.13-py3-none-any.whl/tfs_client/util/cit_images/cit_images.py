from typing_extensions import Unpack
import base64
import os
from ...http import Params
from ..postprocessing import multi_predict

def read64(path: str) -> str:
  """Read an image as URL-safe base64"""
  with open(path, 'rb') as f:
    bytes = f.read()
    return base64.urlsafe_b64encode(bytes).decode()
  
def box_path(player: int = 0, ply: int = 0, images_path: str = 'images'):
  """Box path (use with `cit images`)"""
  return os.path.join(images_path, 'boxes', f'boxes-{player}-{ply}.jpg')

def read_boxes(players = range(2), plys = range(8), images_path: str = './images') -> list[tuple[str, ...]]:
  plys = list(plys)
  return [
    tuple(read64(box_path(player, ply, images_path)) for player in players)
    for ply in plys
  ]

async def batch_predict(from_ply: int, to_ply: int, images_path: str = './images', **p: Unpack[Params]) -> list[list[list[tuple[str, float]]]]:
  imgs = read_boxes(plys=range(from_ply, to_ply), images_path=images_path)
  return await multi_predict(imgs, **p)