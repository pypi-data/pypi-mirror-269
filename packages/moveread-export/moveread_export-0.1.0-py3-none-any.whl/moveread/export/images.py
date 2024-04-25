from haskellian import Either, Left, Right, promise as P
from scoresheet_models import ModelID
import pure_cv as vc
from cv2 import Mat
from kv.api import KV
from moveread.core import Image
from moveread.boxes import export, exportable
from moveread.errors import MissingMeta

@P.lift
async def image_boxes(
  image: Image, model: ModelID | None = None, *, blobs: KV[bytes]
) -> Either[MissingMeta, list[Mat]]:
  if image.meta is None:
    return Left(MissingMeta('Empty image meta'))
  match exportable(image.meta, model):
    case Left(err):
      return Left(err)
    case Right(ann):
      img = (await blobs.read(image.url)).unsafe()
      mat = vc.decode(img)
      return Right(export(mat, ann))