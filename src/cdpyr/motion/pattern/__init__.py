from cdpyr.motion.pattern.pattern import Pattern

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"

MP_1T = Pattern(1, 0)
MP_2T = Pattern(2, 0)
MP_3T = Pattern(3, 0)
MP_1R2T = Pattern(2, 1)
MP_2R3T = Pattern(3, 2)
MP_3R3T = Pattern(3, 3)

__all__ = [
        'Pattern',
        'MP_1T',
        'MP_2T',
        'MP_3T',
        'MP_1R2T',
        'MP_2R3T',
        'MP_3R3T',
]
