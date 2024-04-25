from cv2 import Mat
from .annotations import ExportableAnnotations
from robust_extraction import extract_contours
from scoresheet_models import models
from .model_extract import extract_grid, Pads

def export(img: Mat, ann: ExportableAnnotations, pads: Pads | None = None) -> list[Mat]:
  """Export an image's boxes"""
  if ann.tag == 'grid':
    return extract_grid(img=img, coords=ann.grid_coords, model=models[ann.model], pads=pads)
  else:
    return extract_contours(img=img, contours=ann.box_contours)