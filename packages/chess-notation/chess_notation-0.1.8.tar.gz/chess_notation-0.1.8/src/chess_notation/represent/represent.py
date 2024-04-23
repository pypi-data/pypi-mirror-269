from pydantic import BaseModel
from ..styles import Check, Mate, Castle, PawnCapture, PieceCapture, CapturedPiece, \
  is_castle, is_pawn_capture, is_piece_capture, is_check, is_mate, \
  castle, pawn_capture, piece_capture, check, mate
from ..language import Language, translate

class KingEffectStyles(BaseModel):
  checks: list[Check] = ['NONE']
  mates: list[Mate] = ['NONE']

class MotionStyles(BaseModel):
  castles: list[Castle] = ['O-O', 'OO']
  pawn_captures: list[PawnCapture] = ['de', 'de4', 'dxe', 'dxe4', 'PxN', 'xe4']
  piece_captures: list[PieceCapture] = ['Ne4', 'Nxe4', 'NxN']

def motion_representations(san: str, motions: MotionStyles = MotionStyles(), captured_piece: CapturedPiece = None) -> set[str]:
  outputs = set([san])

  if is_castle(san):
    for style in motions.castles:
      outputs.add(castle(san, style))
  elif is_pawn_capture(san):
    for style in motions.pawn_captures:
      outputs.add(pawn_capture(san, style, captured_piece))
  elif is_piece_capture(san):
    for style in motions.piece_captures:
      outputs.add(piece_capture(san, style, captured_piece))

  return outputs

def effect_representations(san: str, effects: KingEffectStyles = KingEffectStyles()) -> set[str]:
  outputs = set([san])

  if is_check(san):
    for style in effects.checks:
      outputs.add(check(san, style))
  elif is_mate(san):
    for style in effects.mates:
      outputs.add(mate(san, style))
  
  return outputs

def representations(
  san: str,
  motions: MotionStyles = MotionStyles(),
  effects: KingEffectStyles = KingEffectStyles(),
  languages: list[Language] = ['CA', 'EN'],
  captured_piece: CapturedPiece | None = None
) -> set[str]:
  return {
    translate(styled, lang)
    for motioned in motion_representations(san, motions, captured_piece)
    for styled in effect_representations(motioned, effects)
    for lang in languages
  }