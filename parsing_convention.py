
# The conversion marker signifies that the DWG/DXF component is to be included in the conversion.
# Any object name not beginning with this character is skipped during conversion.
CONVERSION_MARKER = '&'

# The component divider is the character that separates the location from the component id.
COMPONENT_DIVIDER = '/'

# The TYPES dictionary is built so that the keys signify what component code corresponds to a 
# component type and whether it's drawn graphically in the SVG or simply put down as a data tag.
# For instance, "C1" : {"component1", False} 
# means the component id C1 has the component type name component1, and isn't drawn graphically in the SVG.
TYPES = {
    "C1": ["component1", False],
    "C2": ["component2", True],
    "C3": ["component3", True],
    "C4": ["component4", False],
}



