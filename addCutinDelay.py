"""
This Script is meant to add a delay or slow-down for cuts intended to penetrate with the laser.
The reason for this is because the laser can cut at a faster speed after the cut has already penetrated the material.
"""
import BaseParser

class PenetrationDelayParser(BaseParser):
    def begin_cut:

