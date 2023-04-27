"""_____________________________________________________________________

:PROJECT: LabOP Device Ontology

* Terminology box of the Device Ontology *

:details:  Main module implementation.

            python module that defines an ontology of common device classes that are used in a scientific lab, based on EMMOntoPy
            it should be possible to use this ontology to automatically get the right SI units for the properties of the device
            and to automatically get the right EMMO classes for the device
            as much as possible, the ontology should be based on EMMO, but it may be necessary to add some classes and properties
            that are not in EMMO
            as much as possible should be inferred from EMMO, but it may be necessary to add some axioms
            the ontology should be able to be used in a lab notebook, and should be able to be used to automatically generate
            a device inventory
            the ontology should be able to be used to automatically generate a device database


.. note:: -
.. todo:: - 
________________________________________________________________________
"""


import os
import pathlib
import logging

from ontopy import World
from ontopy.utils import write_catalog

from labop_device_ontology.emmo_utils import en, pl

from owlready2 import DatatypeProperty, FunctionalProperty, ObjectProperty, AllDisjoint, Thing

from labop_device_ontology import __version__ # Version of this ontology
from labop_device_ontology.export_ontology import export_ontology

class LOLabwareTBox:
    def __init__(self, lw_tbox_filename: str = None, emmo_world=None, emmo=None, emmo_url: str = None) -> None:

        self.emmo = emmo
        self.emmo_url = emmo_url
        
        self.base_iri = 'http://www.labop.org/labop_device_tbox'

        print("LOLabwareTBox:lw_tbox_filename:", lw_tbox_filename)

        if lw_tbox_filename is None:
            self.lodevt = emmo_world.get_ontology(self.base_iri)
        else:
            self.lodevt = emmo_world.get_ontology(lw_tbox_filename).load()

        self.emmo.imported_ontologies.append(self.lodevt)
        self.emmo.sync_python_names()
        
        # --- ontology definition

        if lw_tbox_filename is None:
            # define the ontology
            print("++++++ defining ontology")
            self.define_ontology()

    def export(self, path: str = ".", format='turtle') -> None:
        """save ontology """
        export_ontology(ontology=self.lodevt, path=path, onto_base_filename='labop_device_tbox', format=format, emmo_url=self.emmo_url)

    def define_ontology(self):
        """defining the  labOP-device ontology Terminology Box (TBox) """
        logging.debug('defining device ontology')

        with self.lodevt:

            # Terminology Components (TBox) 


            # device visual representation
            
            class ModelIcon(Thing):
                """Icon of the device in X format. SVG ?"""
            

            class Model2D(Thing):
                """2D model of the device in X format. SVG ?"""

            class Model3D(Thing):
                """3D model of the device in X format. STL ?"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/3D_modeling")

            
            # AllDisjoint([ModelIcon, Model2D, Model3D])


            class ShapePolygonXY(Thing):
                """Generalized shape polygon for more complex well shapes, in xy plane / direction."""

            class ShapePolygonZ(Thing):
                """Generalized shape polygon for more complex well shapes, in z direction = rotation axis."""

            class ShapeModel2D(Thing):
                """2D model of Well shape"""

            class ShapeModel3D(Thing):
                """3D model of Well shape"""

            class FirstInteractionPosition(self.emmo.Vector):
                """Position of first interaction point of a pipette tip with a well or a needle with a septum, rel. to the upper left corner of the device. - what about round device?"""


           

            # Device Vendor related properties
            # =================================

            class Vendor(Thing):
                """Device Vendor"""

            class VendorProductNumber(Thing):
                """Device Vendor Product Number"""

            # UNSPSC
            class UNSPSC(Thing):
                """United Nations Standard Products and Services Code (UNSPSC) for device"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/UNSPSC")

            # eCl@ss
            class EClass(Thing):
                """eCl@ss for device"""
                wikipediaEntry = en("https://en.wikipedia.org/wiki/EClass")


            # Device Classes
            # ====================

            # Basic ------

            class Device(self.emmo.Device):
                """Device is a physical object that is used in a scientific lab, and that is not a consumable. It can be a single object or a set of objects that are used together. """
                wikipediaEntry = en("https://en.wikipedia.org/wiki/Device")

                # is_a = [self.lodev.has_Material.some(str),
                #         self.lodev.has_NumCols.some(int),
                #         self.lodev.has_NumRows.some(int)]

            #  Relations / Properties
            # ========================

            # Physical Properties

            #class hasLength:
                # """"Device total length """
                # is_a = [
                #     self.lodev.hasReferenceUnit.only(
                #         self.lodev.hasPhysicalDimension.only(self.lodev.Length)
                #     ),
                #     hasType.exactly(1, self.lodev.Real), ]

            # class hasWidth(FunctionalProperty):
            #     """Device total width, """
            #     domain = [Device]
            #     range = [Width]

            # class hasHeight(Device >> self.lodev.Height, FunctionalProperty):
            #     """Device total hight, without  any additions, like lids etc. """

            # class hasLengthTolerance(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
            #     """Device length tolerance."""

            class hasLength(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device total length, without  any additions, like lids etc."""
                

            class hasLengthTolerance(self.emmo.Length >> float, FunctionalProperty, DatatypeProperty):
                """Device relative length tolerance (= measured width/target width)."""
            
            class hasWidth(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device total width, without  any additions, like lids etc."""
            
            class hasWidthTolerance(self.emmo.Length >> float, FunctionalProperty, DatatypeProperty):
                """Device relative width tolerance (= measured width/target width)."""
            
            class hasHeight(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device total hight, without  any additions, like lids etc. """

            class hasHeightTolerance(self.emmo.Length >> float, FunctionalProperty, DatatypeProperty):
                """Device height tolerance."""

            class hasGrippingHeight(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device total hight, without  any additions, like lids etc. """

            class hasGrippingHeightLidding(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device total hight, without  any additions, like lids etc. """
            
            class hasGrippingHeightWithLid(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device total hight, without  any additions, like lids etc. """

            class hasGrippingPressure(Device >> self.emmo.Pressure, FunctionalProperty, ObjectProperty):
                """Device max gripping pressure."""

            class hasRadiusXY(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device radius of a round shape in XY direction """

            class hasRadiusZ(Device >> self.emmo.Length, FunctionalProperty, ObjectProperty):
                """Device radius of a round shape in XY direction """

            class hasVolume(Device >> float, FunctionalProperty):
                """Total Device volume """

            class hasHightLidded(Device >> float, FunctionalProperty):
                """Device total hight, with additions, like lids etc."""

            class hasHightStacked(Device >> float, FunctionalProperty):
                """Device stacking height without any additions, like lids."""

            class hasHightStackedLidded(Device >> float, FunctionalProperty):
                """Device stacking height with additions, like lids."""

            class hasMass(Device >> float, FunctionalProperty):
                """Mass of the Device """

            class hasMaxSheerForce(Device >> self.emmo.Force, FunctionalProperty):
                """Max sheer force of the Device, e.g. during centrifugation"""

            class hasCoatingMaterial(Device >> str, FunctionalProperty):
                """Device coating material"""

            
            class hasColorDescription(Device >> str, FunctionalProperty):
                """Device color description, e.g. white, black, opaque, blue, transparent, ..."""

            class hasColorRGB(Device >> str, FunctionalProperty):
                """Device color in RGB hex encoding"""

            class isLiddable(Device >> bool, FunctionalProperty):
                """device is liddable"""

            class isStackable(Device >> bool, FunctionalProperty):
                """device is stackable"""

            class isSealable(Device >> bool, FunctionalProperty):
                """container is sealable"""

            class hasSetptum(Device >> bool, FunctionalProperty):
                """Setptum of the Device"""

            class hasMaterial(Device >> str, DatatypeProperty):
                """Polymer, properties, like solvent tolerance, transparency, ...."""

            class hasSeptumMaterial(Device >> str, FunctionalProperty):
                """Septum material"""

            class hasSeptumPenetrationForce(Device >> self.emmo.Force, FunctionalProperty):
                """Septum penetration force"""



            class hasNumCols(Device >> int, FunctionalProperty):
                """Number of Columns of muti-well device"""

            class hasNumRows(Device >> int, FunctionalProperty):
                """Number of Rows of Device"""

            class hasNumWells(Device >> int, FunctionalProperty):
                """Number of Wells of muti-well device"""

            # Production Properties / Metadata

            class hasManufacturer(Device >> str, FunctionalProperty):
                 """Name of the Manufacturer """
            
            class isProductType(Device >> str, FunctionalProperty):
                """Device product Type"""

            class hasModelID(Device >> str, FunctionalProperty):
                """Device model ID/number"""

            class hasProductID(Device >> str, FunctionalProperty):
                """Manufacturer Product ID/Number of the Device"""

            # multiwell device properties

            class hasWellVolume(Device >> float, FunctionalProperty):
                """Total Device volume """

            class hasA1Position(Device >> str, FunctionalProperty):
                """Device A1 position"""

            class hasWellDistRow(Device >> float, FunctionalProperty):
                """wWll-to-well distance in row direction"""
            
            class hasWellDistCol(Device >> float, FunctionalProperty):
                """"Well-to-well distance in column direction"""

            # Well properties of device with wells
            class hasDepthWell(Device >> float, FunctionalProperty):
                """Well total well depth=hight"""
            
            class hasShapeWell(Device >> str, FunctionalProperty):
                """Well overall / top well shape,e.g. round, square, buffeled,..."""
            
            class hasShapeWellBottom(Device >> str, FunctionalProperty):
                """Well, bottom shape, flat, round, conical-"""

            class hasTopRadiusXY(Device >> float, FunctionalProperty):
                """Well radius of a round well at the top opening in x-y plane."""

            class hasBottomRadiusXY(Device >> float, FunctionalProperty):
                """Radius of a round bottom in xy plane / direction."""

            class hasBottomRadiusZ(Device >> float, FunctionalProperty):
                """Radius of a round bottom in z (hight) direction."""

            class hasConeAngle(Device >> float, FunctionalProperty):
                """Opening angle of cone in deg."""

            class hasConeDepth(Device >> float, FunctionalProperty):
                """Depth of cone from beginning of conical shape."""

            class hasShapePolygonXY(Device >> float, FunctionalProperty):
                """Generalized shape polygon for more complex well shapes, in xy plane / direction."""

            class hasShapePolygonZ(Device >> str, FunctionalProperty):
                """Generalized shape polygon for more complex well shapes, in z direction = rotation axis."""

            class hasShapeModel2D(Device >> str, FunctionalProperty):
                """2D model of Well shape"""

            class hasShapeModel3D(Device >> str, FunctionalProperty):
                """3D model of Well shape"""

            class hasImageLink(Device >> str, FunctionalProperty):
                """Link to image of the Device"""

            # device with screw cap

            class hasScrewCap(Device >> bool, FunctionalProperty):
                """Screw cap type"""

            class hasScrewCapMaterial(Device >> str, FunctionalProperty):
                """Screw cap material"""
            
            class hasScrewCapColor(Device >> str, FunctionalProperty):
                """Screw cap color"""


            # device with snap cap


            # vendor specific properties
            class hasVendorName(Device >> str, FunctionalProperty):
                """Vendor name"""
            class hasVendorProductID(Device >> str, FunctionalProperty):
                """Vendor Product ID"""
            class hasUNSPSC(Device >> str, FunctionalProperty):
                """UNSPSC code"""

            class hasEClass(Device >> str, FunctionalProperty):
                """EClass code"""

            class hasEAN(Device >> str, FunctionalProperty):
                """EAN code"""

            
            # further properties:

            # lengthAtEdge, lengthOverall, isSLAS1-2004complian

            # isSLAS1-2004compliant

            # all disjoined properties

            # special device classes
            # can be used for faster type testing


            # Location of the device

            class Building(self.emmo.Building):
                pass

            class Laboratory(self.emmo.Laboratory):
                pass

            class Room(self.emmo.Room):
                pass
           
            

                

            



            
