# This file is part of dsiUnits (https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
import re
import warnings
import difflib
from typing import List
from copy import deepcopy
import math
from fractions import Fraction
import numbers


def _dsiStrFromNodes(nodeList):
    """Converts a list of nodes to a D-SI string."""
    dsiStr = ""
    for i, fraction in enumerate(nodeList):
        if i > 0:
            dsiStr += r"\per"
        for node in fraction:
            dsiStr += str(node)
    return dsiStr


class dsiParser:
    __dsiVersion = "2.2.0"
    __dsiSchemaUrl = "https://www.ptb.de/si/v2.2.0/SI_Format.xsd"
    __dsiRepositoryURL = "https://gitlab1.ptb.de/d-ptb/d-si/xsd-d-si"
    """Parser to parse D-SI unit string into a tree
    """

    def __init__(self, latexDefaultWrapper='$$', latexDefaultPrefix='', latexDefaultSuffix=''):
        """
        Args:
            latexDefaultWrapper (str, optional): String to be added both in the beginning and the end of the LaTeX string. Defaults to '$$'.
            latexDefaultPrefix (str, optional): String to be added in the beginning of the LaTeX string, after the wrapper. Defaults to ''.
            latexDefaultSuffix (str, optional): String to be added in the end of the LaTeX string, before the wrapper. Defaults to ''.
        """
        super()
        self.latexDefaultWrapper = latexDefaultWrapper
        self.latexDefaultPrefix = latexDefaultPrefix
        self.latexDefaultSuffix = latexDefaultSuffix

    def parse(self, dsiString: str):
        """parses a D-SI string into a tree structure


        Args:
            dsiString (str): D-SI unit raw string

        Raises:
            RuntimeWarning: double backslashes in D-SI string
            RuntimeWarning: empty D-SI string

        Returns:
            dsiTree: dsiTree object containing the D-SI unit
        """
        warningMessages = []
        # Catch any double (triple...) \ before they annoy us
        while r'\\' in dsiString:
            warningMessages.append(
                _warn(f"Double backslash found in string, treating as one backslash: «{dsiString}»", RuntimeWarning))
            dsiString = dsiString.replace(r'\\', '\\')

        if dsiString == "":
            warningMessages.append(_warn("Given D-SI string is empty!", RuntimeWarning))
            return dsiUnit('NULL', [], warningMessages, self.latexDefaultWrapper, self.latexDefaultPrefix,
                           self.latexDefaultSuffix)

        tree = []
        (tree, fractionWarnings) = self._parseDsiFraction(dsiString)
        warningMessages += fractionWarnings
        for i, node in enumerate(tree):
            (tree[i], fractionlessWarnings) = self._parseFractionlessDsi(node)
            warningMessages += fractionlessWarnings
        return dsiUnit(dsiString, tree, warningMessages, self.latexDefaultWrapper, self.latexDefaultPrefix,
                       self.latexDefaultSuffix)

    def _parseDsiFraction(self, dsiString: str):
        """parses D-SI fraction into list of fraction elements

        Args:
            dsiString (str): D-SI unit raw string

        Raises:
            RuntimeWarning: String must not contain more than one "per",
                            as defined in the D-SI specs

        Returns:
            list: strings separated by the "per"
            list: warning messages of problems encountered while parsing
        """
        tree = []
        warningMessages = []
        dsiStringWOperCent = dsiString.replace('percent',
                                               'prozent')  # rename percent to prozent to have it not split at per ....
        tree = dsiStringWOperCent.split(r"\per")
        for i, subtree in enumerate(tree):
            tree[i] = tree[i].replace('prozent', 'percent')
        for subtree in tree:
            if len(subtree) == 0:
                warningMessages.append(_warn(r"The dsi string contains a \per missing a numerator or denominator! " +
                                             f"Given string: {dsiString}",
                                             RuntimeWarning))
                tree.remove(subtree)
        if len(tree) > 2:
            warningMessages.append(_warn(r"The dsi string contains more than one \per, does not " +
                                         f"match specs! Given string: {dsiString}",
                                         RuntimeWarning))
        return (tree, warningMessages)

    def _parseFractionlessDsi(self, dsiString: str):
        """parses D-SI unit string without fractions

        Args:
            dsiString (str): D-SI unit raw string, not containing any fractions

        Raises:
            RuntimeWarning: if string does not meet the specs

        Returns:
            list: list of nodes
            list: warning messages of problems encountered while parsing
        """
        warningMessages = []
        items = dsiString.split("\\")
        if items[0] == '':  # first item of List should be empty, remove it
            items.pop(0)
        else:
            warningMessages.append(
                _warn(f"string should start with \\, string given was «{dsiString}»", RuntimeWarning))
        nodes = []

        (prefix, unit, exponent) = ('', '', '')
        item = items.pop(0)
        while True:
            if item in _dsiPrefixesLatex:
                prefix = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if item in _dsiUnitsLatex:
                unit = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if re.match(r'tothe\{-?\d+\.?\d?\}', item):
                exponent = item.split('{')[1].split('}')[0]
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            elif re.match(r'tothe\{.*\}', item):
                exponent = item.split('{')[1].split('}')[0]
                try:
                    floatCast = float(exponent)
                except ValueError:
                    warningMessages.append(_warn(f"The exponent «{exponent}» is not a number!", RuntimeWarning))
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
            if (prefix, unit, exponent) == ('', '', ''):
                unit = item
                try:
                    item = items.pop(0)
                except IndexError:
                    item = ''
                closestMatches = _getClosestStr(unit)
                if len(closestMatches) > 0:
                    closestMatchesStr = ', \\'.join(closestMatches)
                    closestMatchesStr = '\\' + closestMatchesStr
                    warningMessages.append(_warn(
                        fr"The identifier «{unit}» does not match any D-SI units! Did you mean one of these «{closestMatchesStr}» ?",
                        RuntimeWarning))
                else:
                    warningMessages.append(
                        _warn(fr"The identifier «{unit}» does not match any D-SI units!", RuntimeWarning))
            elif unit == '':
                itemStr = ""
                if prefix != "":
                    itemStr = itemStr + "\\" + prefix
                if exponent != "":
                    itemStr = itemStr + r"\tothe{" + exponent + r"}"
                warningMessages.append(
                    _warn(f"This D-SI unit seems to be missing the base unit! «{itemStr}»", RuntimeWarning))

            nodes.append(_node(prefix, unit, exponent))
            if (len(items) == 0) and (item == ''): break
            (prefix, unit, exponent) = ('', '', '')
        return (nodes, warningMessages)

    def info(self):
        infoStr = "D-SI Parser Version: " + str(self) + "using D-SI Schema Version: " + str(
            self.__dsiVersion) + "from: " + str(self.__dsiRepositoryURL) + "using D-SI Schema: " + str(
            self.__dsiSchemaUrl)
        print(infoStr)
        return (infoStr, self.__dsiVersion, self.__dsiSchemaUrl, self.__dsiRepositoryURL)

dsiDefaultParser=dsiParser()

class dsiUnit:
    """D-SI representation in tree form, also includes validity check and warnings about D-SI string.
       Tree format: list of lists:
           List format:
           First layer: items of the fraction
           Second layer: nodes containing prefix, unit, power
    """

    def __init__(self, dsiString: str, dsiTree=[], warningMessages=[], latexDefaultWrapper='$$', latexDefaultPrefix='',
                 latexDefaultSuffix=''):
        """
        Args:
            dsiString (str): the D-SI unit string to be parsed
            optional dsiTree (list): List of lists of nodes as tuples containing (prefix: str,unit: str,exponent: float=1.0,scaleFactor: float = 1.0)
            like [('metre', 1.0, 1.0), ('second', -1.0, 1.0)] to generate ms^-1 when usign this construction method no str can be given
        """
        # we have got a tree so we dont need to parse the string
        if dsiString == "" and dsiTree != []:
            dsiString=_dsiStrFromNodes(dsiTree)
        if dsiString != "" and dsiTree == []:
            try:
                dsiTree = dsiDefaultParser.parse(dsiString).tree
                warningMessages = dsiDefaultParser.parse(dsiString).warnings
            except Exception as e:
                warnings.warn(e)
        if dsiString == "" and dsiTree == []:
            warnings.warn("Given D-SI string is empty!")
            dsiTree = dsiDefaultParser.parse(dsiString).tree
            warningMessages = dsiDefaultParser.parse(dsiString).warnings
        self.dsiString = dsiString
        self.tree = dsiTree
        self.warnings = warningMessages
        self.valid = len(self.warnings) == 0
        self._latexDefaultWrapper = latexDefaultWrapper
        self._latexDefaultPrefix = latexDefaultPrefix
        self._latexDefaultSuffix = latexDefaultSuffix




    def toLatex(self, wrapper=None, prefix=None, suffix=None):
        """converts D-SI unit string to LaTeX

        Args:
            wrapper (str, optional): String to be added both in the beginning and the end of the LaTeX string. Defaults to the value set in the parser object.
            prefix (str, optional): String to be added in the beginning of the LaTeX string, after the wrapper. Defaults to the value set in the parser object.
            suffix (str, optional): String to be added in the end of the LaTeX string, before the wrapper. Defaults to the value set in the parser object.

        Returns:
            str: the corresponding LaTeX code
        """

        # If no wrapper/prefix/suffix was given, set to the parser's default
        wrapper = self._latexDefaultWrapper if wrapper == None else wrapper
        prefix = self._latexDefaultPrefix if prefix == None else prefix
        suffix = self._latexDefaultSuffix if suffix == None else suffix

        if self.tree == []:
            if len(prefix) + len(suffix) > 0:
                return wrapper + prefix + suffix + wrapper
            else:
                return ""
        latexArray = []
        if len(self.tree) == 1:  # no fractions
            for node in self.tree[0]:
                latexArray.append(node.toLatex())
            latexString = r'\,'.join(latexArray)
        elif len(self.tree) == 2:  # one fraction
            latexString = ""
            latexString += r'\frac'
            for frac in self.tree:
                latexString += r'{'
                nodeArray = []
                for node in frac:
                    nodeArray.append(node.toLatex())
                latexString += r'\,'.join(nodeArray)
                latexString += r'}'
        else:  # more than one fraction
            latexString = ""
            for i in range(len(self.tree)):
                nodeArray = []
                if i > 0:
                    latexString += r'{\color{red}/}'
                for node in self.tree[i]:
                    nodeArray.append(node.toLatex())
                latexString += r'\,'.join(nodeArray)
        return wrapper + prefix + latexString + suffix + wrapper

    def toUTF8(self):
        """Converts D-SI unit string to a compact UTF-8 format."""

        def exponent_to_utf8(exp):
            """Converts numerical exponents to UTF-8 subscript."""
            # Mapping for common exponents to UTF-8
            superscripts = {"1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵",
                            "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "0": "⁰",
                            "-": "⁻",".": "˙"}
            # Convert fractional exponents to a more readable format if needed
            exp_str = str(exp).rstrip('.0')  # Remove trailing '.0' for whole numbers
            return ''.join(superscripts.get(char, char) for char in exp_str)

        utf8Array = []
        for fraction in self.tree:
            fractionUtf8Array = []
            for node in fraction:
                # Fetch UTF-8 unit representation
                unitStr = _dsiUnitsUTF8.get(node.unit, node.unit)

                # Handle prefix (if any) and unit
                prefixStr = _dsiPrefixesUTF8.get(node.prefix, node.prefix) if node.prefix else ""
                utf8Str = f"{prefixStr}{unitStr}"  # Direct concatenation for compactness

                # Handle exponent, converting to UTF-8 subscript, if not 1
                if node.exponent and node.exponent != 1:
                    utf8Str += exponent_to_utf8(node.exponent)

                fractionUtf8Array.append(utf8Str)

            # Join units within the same fraction with a dot for compactness
            utf8Array.append("".join(fractionUtf8Array))

        # Handle fractions, join numerator and denominator with a slash for division
        return " / ".join(utf8Array).replace(' ', '')



    def toBaseUnitTree(self,complete=False):
        """
        Converts the entire D-SI tree to its base unit representation.
        """
        baseUnitTree = []
        for fraction in self.tree:
            baseFraction = []
            for node in fraction:
                baseFraction.extend(node.toBaseUnits())
            baseUnitTree.append(baseFraction)
        unconsolidatedTree = dsiUnit(self.dsiString, baseUnitTree, self.warnings, self._latexDefaultWrapper, self._latexDefaultPrefix, self._latexDefaultSuffix)
        reduced=unconsolidatedTree.reduceFraction()
        # if kgms True we do a second round but resolve volt ampere mole this round
        if complete:
            baseUnitTree = []
            for fraction in self.tree:
                baseFraction = []
                for node in fraction:
                    baseFraction.extend(node.toBaseUnits(complete=complete))
                baseUnitTree.append(baseFraction)
            unconsolidatedTree = dsiUnit(self.dsiString, baseUnitTree, self.warnings, self._latexDefaultWrapper,
                                         self._latexDefaultPrefix, self._latexDefaultSuffix)
            reduced = unconsolidatedTree.reduceFraction()
        return reduced

    def reduceFraction(self):
        """
        Creates a new _dsiTree instance with reduced fractions.
        - For a single node: Simply copies it to the consolidated list.
        - For two nodes: Copies the first node and adds the second node with its exponent multiplied by -1.
        - For more than two nodes: Raises a RuntimeError.
        - Consolidates nodes with the same base unit by multiplying scales and summing exponents.
        - Sorts the nodes alphabetically by unit.
        - The first node carries the overall scale factor.
        """
        if len(self.tree) > 2:
            raise RuntimeError("D-SI tree with more than two fractions cannot be reduced.")

        consolidated_nodes = []

        # Handling single and two-node cases
        if len(self.tree) == 1:
            consolidated_nodes = self.tree[0]
        elif len(self.tree) == 2:
            # Copy nodes from the first fraction
            consolidated_nodes = [node for node in self.tree[0]]

            # Copy nodes from the second fraction, adjusting the exponents
            for node in self.tree[1]:
                # Inverting the exponent for nodes in the denominator
                invertedExponent = -1 * node.exponent
                fractionalScaleFactor = 1 / node.scaleFactor
                consolidated_nodes.append(_node(node.prefix, node.unit, invertedExponent, fractionalScaleFactor))

        # Consolidating nodes with the same unit
        i = 0
        while i < len(consolidated_nodes):
            j = i + 1
            while j < len(consolidated_nodes):
                if consolidated_nodes[i].unit == consolidated_nodes[j].unit:
                    # Consolidate nodes
                    scaleFactor = consolidated_nodes[i].scaleFactor*consolidated_nodes[j].scaleFactor
                    consolidated_nodes[i].scaleFactor = scaleFactor
                    exponent=consolidated_nodes[i].exponent + consolidated_nodes[j].exponent
                    consolidated_nodes[i].exponent = exponent
                    del consolidated_nodes[j]
                else:
                    j += 1
            i += 1

        # Calculate overall scale factor and apply it to the first node
        overall_scale_factor = 1.0
        for node in consolidated_nodes:
            overall_scale_factor *= node.scaleFactor
            node.scaleFactor = 1.0  # Reset scale factor for individual nodes



        # Sort nodes alphabetically by unit
        consolidated_nodes.sort(key=lambda x: x.unit)
        # Apply overall scale factor to the first node, if it exists
        if consolidated_nodes:
            consolidated_nodes[0].scaleFactor = overall_scale_factor
        nodesWithOutpowerZero=[]
        for node in consolidated_nodes:
            if node.exponent != 0:
                nodesWithOutpowerZero.append(node)
        if len(nodesWithOutpowerZero) == 0: # ok all noes have ben power of zero so we deleted them so we end up with one as unit and 1.0 as exponent
            nodesWithOutpowerZero.append(_node("", "one", 1.0,scaleFactor=overall_scale_factor))
        consolidated_nodes=nodesWithOutpowerZero
        # Create and return a new instance of _dsiTree with consolidated nodes
        return dsiUnit(self.dsiString, [consolidated_nodes], self.warnings, self._latexDefaultWrapper,
                       self._latexDefaultPrefix, self._latexDefaultSuffix)
    def sortTree(self):
        """Sorts each fraction's nodes alphabetically by their units."""
        for fraction in self.tree:
            fraction.sort(key=lambda node: node.unit)
    def __eq__(self, other):
        """Checks if two D-SI trees are identical after sorting their nodes alphabetically."""
        if not isinstance(other, dsiUnit):
            return False

        # Sort both trees before comparison
        selfCopy = deepcopy(self)
        otherCopy = deepcopy(other)
        selfCopy.sortTree()
        otherCopy.sortTree()
        if selfCopy.tree == otherCopy.tree:
            return True
        else:
            scalfactor,baseunit=selfCopy.isScalablyEqualTo(otherCopy)
            if scalfactor == 1.0:
                return True
            else:
                return False

    def isScalablyEqualTo(self, other,complete=False):
        """Checks if two D-SI trees are scalably equal.

        Returns:
            (bool, float): Tuple of a boolean indicating if trees are scalably equal, and the scale factor.
        """
        if not isinstance(other, dsiUnit):
            return (math.nan, None)


        sortedself=deepcopy(self)
        sortedself.sortTree()
        sortedother=deepcopy(other)
        sortedother.sortTree()
        # okay now check if is identical
        if sortedself.tree == sortedother.tree:
            return (1.0,self)
        scalefactor=1
        for fracIdx,fraction in enumerate(sortedself.tree):
            try:
                if len(fraction) != len(sortedother.tree[fracIdx]):
                    scalefactor=math.nan
                    break
                for nodeIDX,node in enumerate(fraction):
                    scalefactor *= node.isScaled(sortedother.tree[fracIdx][nodeIDX])
            except IndexError:
                # if we get here we have a fraction in one tree that is not in the other in this case we resolve to base units and compare
                scalefactor=math.nan
                break
        if not math.isnan(scalefactor):
            return (scalefactor,self)
        # Convert both trees to their base unit representations
        selfBaseUnitTree = self.toBaseUnitTree(complete=complete)
        otherBaseUnitTree = other.toBaseUnitTree(complete=complete)

        # Sort both trees
        selfBaseUnitTree.sortTree()
        otherBaseUnitTree.sortTree()
        # Check ifunits match
        if len(selfBaseUnitTree.tree) != len(otherBaseUnitTree.tree):
            return (math.nan, None)
        # Calculate scale factor
        scaleFactor = 1.0
        if len(selfBaseUnitTree.tree) != 1 or len(otherBaseUnitTree.tree) != 1:
            raise RuntimeError("D-SI tree with more than one fraction cannot be compared. And should not existhere since we consolidatet earlyer")
        for selfNode, otherNode in zip(selfBaseUnitTree.tree[0], otherBaseUnitTree.tree[0]):
            if selfNode.unit != otherNode.unit:
                return (math.nan, None)
            if float(selfNode.exponent) != float(otherNode.exponent):
                return (math.nan, None)
            scaleFactor *= otherNode.scaleFactor / selfNode.scaleFactor
        # reseting scalfactor to 1.0
        for fraction in selfBaseUnitTree.tree:
            for node in fraction:
                node.scaleFactor = 1.0
        return (scaleFactor,selfBaseUnitTree)

    def __str__(self):
        result = ""
        for node in self.tree[0]:
            result += str(node)
        if len(self.tree) == 2:
            result += r'\per'
            for node in self.tree[1]:
                result += str(node)
        return result

    def __repr__(self):
        contentStr=self.toUTF8()
        if not self.valid:
            contentStr+=' INVALIDE'
        if self.warnings:
            contentStr+=f" {len(self.warnings)} WARNINGS"
        # Simple representation: class name and D-SI string
        return f"{contentStr}"


    def __pow__(self, other):
        if not isinstance(other, numbers.Real):
            raise TypeError("Exponent must be a real number")
        resultNodeLIst = deepcopy(self.tree)
        for fraction in resultNodeLIst:
            for node in fraction:
                node.exponent *= other
        resultTree =dsiUnit("", resultNodeLIst, self.warnings, self._latexDefaultWrapper, self._latexDefaultPrefix, self._latexDefaultSuffix)
        resultTree = resultTree.reduceFraction()
        return resultTree

    def __mul__(self, other):
        resultNodeLIst=deepcopy(self.tree)
        for i,fraction in enumerate(other.tree):
            if i>1:
                raise RuntimeError("D-SI tree with more than one fraction cannot be multiplied")
            try:
                resultNodeLIst[i].extend(deepcopy(fraction))
            except IndexError:
                resultNodeLIst.append(deepcopy(fraction))# there was no fraction so we add it

        resultTree =dsiUnit("", resultNodeLIst, self.warnings, self._latexDefaultWrapper, self._latexDefaultPrefix, self._latexDefaultSuffix)
        resultTree = resultTree.reduceFraction()
        return resultTree

    def __truediv__(self, other):
        return self * other**-1


class _node:
    """one node of the D-SI tree, containing prefix, unit, power
    """
    def __init__(self,    prefix: str,unit: str,exponent: float=1.0,scaleFactor: float = 1.0  ):# Adding scale factor with default value 1.0
        self.prefix=prefix
        self.unit=unit
        if isinstance(exponent,float) or isinstance(exponent,int):
            self.exponent=float(exponent)
        if isinstance(exponent,str):
            if exponent== '':
                exponent= 1.0
            else:
                try:
                    exponent=float(exponent)
                except ValueError:
                    exponent=exponent
                    warnings.warn(f"Exponent «{exponent}» is not a number!", RuntimeWarning)
        self.exponent=exponent
        self.scaleFactor=scaleFactor  # Adding scale factor with default value 1.0

    def toLatex(self):
        """generates a latex string from a node

        Returns:
            str: latex representation
        """
        latexString = ""
        if self.prefix:
            latexString += _dsiPrefixesLatex[self.prefix]
        try:
            latexString += _dsiUnitsLatex[self.unit]
        except KeyError:
            latexString += r'{\color{red}\mathrm{'+self.unit+r'}}'
        if isinstance(self.exponent,str):
            #exponet is str this souldnt happen!
            latexString += r'^{{\color{red}\mathrm{'+self.exponent+r'}}}'
        elif self.exponent != 1.0:
            if not self.exponent.is_integer():
                if self.exponent == 0.5:
                    latexString = r'\sqrt{' + latexString + r'}'
                else:
                    exponent_fraction = Fraction(self.exponent).limit_denominator()
                    if exponent_fraction.denominator == 1:
                        # If the denominator is 1, it's effectively an integer
                        latexString += r'\sqrt['+str(int(exponent_fraction.numerator))+']{' + latexString + r'}'
                    else:
                        # For non-integer exponents, display as fractions
                        if int(exponent_fraction.numerator) == 1:
                            latexString += r'\sqrt[' + str(int(exponent_fraction.denominator)) + ']{' + latexString + r'}'
                        else:
                            latexString += r'\sqrt[' + str(
                                int(exponent_fraction.denominator)) + ']{' + latexString + '^{' + str(int(exponent_fraction.numerator)) + '}' + r'}'
            else:
                #TODO better formating
                latexString += r'^{' + str(int(self.exponent)) + r'}'

        
        if self.unit == "":
            latexString = r'{\color{red}'+latexString+r'}'

        return latexString

    def toBaseUnits(self, complete=False) -> List['_node']:
        """
        Converts this node to its base unit representation.
        Adjusts the scale factor during the conversion. Optionally resolves to kg, s, and m units,
        including converting ampere, volt, and mole to their kg, s, and m equivalents when kgs is True.

        Args:
            kgs (bool): If true, also resolves volt to kg, s, and m units.

        Returns:
            List['_node']: List of nodes representing the base units or kg, s, m equivalents.
        """
        # Adjust the scale factor for the prefix
        prefixScale = _dsiPrefixsScales.get(self.prefix, 1)  # Default to 1 if no prefix
        adjustedScaleFactor = self.scaleFactor * prefixScale

        # Convert to base units if it's a derived unit
        if self.unit in _derivedToBaseUnits:
            baseUnitsInfo = _derivedToBaseUnits[self.unit]
            baseUnits = []
            for i, (baseUnit, exponent, scaleFactor) in enumerate(baseUnitsInfo):
                # Apply the adjusted scale factor only to the first base unit
                finalScaleFactor = math.pow(adjustedScaleFactor * scaleFactor, self.exponent) if i == 0 else 1.0
                baseUnits.append(_node('', baseUnit, exponent * self.exponent, finalScaleFactor))
            return baseUnits
        elif complete:
            # Additional logic for converting ampere, volt, and mole to kg, s, and m equivalents
            if self.unit in _additionalConversions:
                kgsUnitsInfo = _additionalConversions[self.unit]
                kgsUnits = []
                for i, (kgsUnit, exponent, scaleFactor) in enumerate(kgsUnitsInfo):
                    finalScaleFactor = math.pow(adjustedScaleFactor * scaleFactor, self.exponent) if i == 0 else 1.0
                    kgsUnits.append(_node('', kgsUnit, exponent * self.exponent, finalScaleFactor))
                return kgsUnits

        # Return the node as is if it's already a base unit, with adjusted scale factor
        return [_node('', self.unit, self.exponent, adjustedScaleFactor)]

    def __eq__(self, other):
        """Checks if two nodes are identical after sorting their nodes alphabetically."""
        return self.prefix == other.prefix and self.unit == other.unit and self.exponent == other.exponent and self.scaleFactor == other.scaleFactor

    def __str__(self):
        result=''

        if self.prefix !='':
            result+='\\'+self.prefix
        result = result + '\\' + self.unit
        if self.exponent != 1.0:
            result =result + r'\tothe{' + '{:g}'.format(self.exponent) + '}'
        return result

    def isScaled(self,other):
        """Checks if two nodes are scaled equal."""
        if self.unit == other.unit and self.exponent == other.exponent:
            return _dsiPrefixsScales[other.prefix]/_dsiPrefixsScales[self.prefix]
        else:
            return math.nan

def _warn(message: str, warningClass):
    """Output warning on command line and return warning message

    Args:
        message (str): warning message
        warningClass: Warning type

    Returns:
        str: message
    """
    warnings.warn(message, warningClass)
    return message

def _getClosestStr(unkownStr):
    """returns the closest string and type of the given string

    Args:
        unknownStr (str): string to be compared

    Returns:
        str: closest string
        str: type of closest string
    """
    possibleDsiKeys = _dsiPrefixesLatex.keys() | _dsiUnitsLatex.keys() | _dsiKeyWords.keys()
    closestStr = difflib.get_close_matches(unkownStr, possibleDsiKeys, n=3,cutoff=0.66)
    return closestStr
# mapping D-SI prefixes to latex
_dsiPrefixesLatex = {
    'deca': r'\mathrm{da}',
    'hecto': r'\mathrm{h}',
    'kilo': r'\mathrm{k}',
    'mega': r'\mathrm{M}',
    'giga': r'\mathrm{G}',
    'tera': r'\mathrm{T}',
    'peta': r'\mathrm{P}',
    'exa': r'\mathrm{E}',
    'zetta': r'\mathrm{Z}',
    'yotta': r'\mathrm{Y}',
    'deci': r'\mathrm{d}',
    'centi': r'\mathrm{c}',
    'milli': r'\mathrm{m}',
    'micro': r'\micro', 
    'nano': r'\mathrm{n}',
    'pico': r'\mathrm{p}',
    'femto': r'\mathrm{f}',
    'atto': r'\mathrm{a}',
    'zepto': r'\mathrm{z}',
    'yocto': r'\mathrm{y}'
}
#TODO maybe directlusing the exponents is better
# mapping D-SI prefixes to scale factors
_dsiPrefixsScales = {
    'yotta': 1e24,
    'zetta': 1e21,
    'exa': 1e18,
    'peta': 1e15,
    'tera': 1e12,
    'giga': 1e9,
    'mega': 1e6,
    'kilo': 1e3,
    'hecto': 1e2,
    'deca': 1e1,
    '':1.0,
    'deci': 1e-1,
    'centi': 1e-2,
    'milli': 1e-3,
    'micro': 1e-6,
    'nano': 1e-9,
    'pico': 1e-12,
    'femto': 1e-15,
    'atto': 1e-18,
    'zepto': 1e-21,
    'yocto': 1e-24
}
# UTF-8 equivalents for SI prefixes
_dsiPrefixesUTF8 = {
    'deca': 'da',
    'hecto': 'h',
    'kilo': 'k',
    'mega': 'M',
    'giga': 'G',
    'tera': 'T',
    'peta': 'P',
    'exa': 'E',
    'zetta': 'Z',
    'yotta': 'Y',
    'deci': 'd',
    'centi': 'c',
    'milli': 'm',
    # Unicode character for micro: 'µ' (U+00B5)
    'micro': 'µ',
    'nano': 'n',
    'pico': 'p',
    'femto': 'f',
    'atto': 'a',
    'zepto': 'z',
    'yocto': 'y'
}
# mapping D-SI units to latex
_dsiUnitsLatex = {
    'metre': r'\mathrm{m}',
    'kilogram': r'\mathrm{kg}',
    'second': r'\mathrm{s}',
    'ampere': r'\mathrm{A}',
    'kelvin': r'\mathrm{K}',
    'mole': r'\mathrm{mol}',
    'candela': r'\mathrm{cd}',
    'one': r'1',
    'day': r'\mathrm{d}',
    'hour': r'\mathrm{h}',
    'minute': r'\mathrm{min}',
    'degree': r'^\circ',
    'arcminute': r"'",
    'arcsecond': r"''",
    'gram': r'\mathrm{g}',
    'radian': r'\mathrm{rad}',
    'steradian': r'\mathrm{sr}',
    'hertz': r'\mathrm{Hz}',
    'newton': r'\mathrm{N}',
    'pascal': r'\mathrm{Pa}',
    'joule': r'\mathrm{J}',
    'watt': r'\mathrm{W}',
    'coulomb': r'\mathrm{C}',
    'volt': r'\mathrm{V}',
    'farad': r'\mathrm{F}',
    'ohm': r'\Omega',
    'siemens': r'\mathrm{S}',
    'weber': r'\mathrm{Wb}',
    'tesla': r'\mathrm{T}',
    'henry': r'\mathrm{H}',
    'degreecelsius': r'^\circ\mathrm{C}',
    'lumen': r'\mathrm{lm}',
    'lux': r'\mathrm{lx}',
    'becquerel': r'\mathrm{Bq}',
    'sievert': r'\mathrm{Sv}',
    'gray': r'\mathrm{Gy}',
    'katal': r'\mathrm{kat}',
    'hectare': r'\mathrm{ha}',
    'litre': r'\mathrm{l}',
    'tonne': r'\mathrm{t}',
    'electronvolt': r'\mathrm{eV}',
    'dalton': r'\mathrm{Da}',
    'astronomicalunit': r'\mathrm{au}',
    'neper': r'\mathrm{Np}',
    'bel': r'\mathrm{B}',
    'decibel': r'\mathrm{dB}',
    'percent':r'\%'
}
# Comprehensive mapping from ASCII/UTF-8 representations to D-SI LaTeX strings
ascii_to_dsi_unit_map = {
    'kg': 'kilogram',
    'm': 'metre',
    's': 'second',
    'A': 'ampere',
    'K': 'kelvin',
    'mol': 'mole',
    'cd': 'candela',
    'g': 'gram',
    'rad': 'radian',
    'sr': 'steradian',
    'Hz': 'hertz',
    'N': 'newton',
    'Pa': 'pascal',
    'J': 'joule',
    'W': 'watt',
    'C': 'coulomb',
    'V': 'volt',
    'F': 'farad',
    'Ω': 'ohm',
    'S': 'siemens',
    'Wb': 'weber',
    'T': 'tesla',
    'H': 'henry',
    '°C': 'degreecelsius',
    'lm': 'lumen',
    'lx': 'lux',
    'Bq': 'becquerel',
    'Gy': 'gray',
    'Sv': 'sievert',
    'kat': 'katal',
    '%': 'percent'
    # Add more units as needed
}

_dsiUnitsUTF8 = {
    'metre': 'm',
    'kilogram': 'kg',
    'second': 's',
    'ampere': 'A',
    'kelvin': 'K',
    'mole': 'mol',
    'candela': 'cd',
    'one': '1',
    'day': 'd',
    'hour': 'h',
    'minute': 'min',
    'degree': '°',
    'arcminute': '′',
    'arcsecond': '″',
    'gram': 'g',
    'radian': 'rad',
    'steradian': 'sr',
    'hertz': 'Hz',
    'newton': 'N',
    'pascal': 'Pa',
    'joule': 'J',
    'watt': 'W',
    'coulomb': 'C',
    'volt': 'V',
    'farad': 'F',
    'ohm': 'Ω',
    'siemens': 'S',
    'weber': 'Wb',
    'tesla': 'T',
    'henry': 'H',
    'degreecelsius': '°C',
    'lumen': 'lm',
    'lux': 'lx',
    'becquerel': 'Bq',
    'sievert': 'Sv',
    'gray': 'Gy',
    'katal': 'kat',
    'hectare': 'ha',
    'litre': 'l',
    'tonne': 't',
    'electronvolt': 'eV',
    'dalton': 'Da',
    'astronomicalunit': 'au',
    'neper': 'Np',
    'bel': 'B',
    'decibel': 'dB',
    'percent': '%'
}

_derivedToBaseUnits = {
    # Time units
    'day': [('second', 1, 86400)],         # 1 day = 86400 seconds
    'hour': [('second', 1, 3600)],         # 1 hour = 3600 seconds
    'minute': [('second', 1, 60)],         # 1 minute = 60 seconds

    # Angle units
    'degree': [('radian', 1, 0.01745329252)], # 1 degree = π/180 radians
    'arcminute': [('radian', 1, 0.0002908882086657216)], # 1 arcminute = π/10800 radians
    'arcsecond': [('radian', 1, 0.00000484813681109536)], # 1 arcsecond = π/648000 radians

    # Mass units
    'gram': [('kilogram', 1, 0.001)],  # 1 gram = 0.001 kilograms

    # Derived units
    'hertz': [('second', -1,1)],  # 1 Hz = 1/s
    'newton': [('kilogram', 1, 1), ('metre', 1, 1), ('second',-2, 1)],  # 1 N = 1 kg·m/s²
    'pascal': [('kilogram', 1, 1), ('metre',-1, 1), ('second',-2, 1)],  # 1 Pa = 1 kg/m·s²
    'joule': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1)],  # 1 J = 1 kg·m²/s²
    'watt': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1)],  # 1 W = 1 kg·m²/s³
    'coulomb': [('second', 1, 1), ('ampere', 1, 1)],  # 1 C = 1 s·A
    'volt': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1), ('ampere',-1, 1)],  # 1 V = 1 kg·m²/s³·A
    'farad': [('kilogram',-1, 1), ('metre',-2, 1), ('second', 4, 1), ('ampere',2, 1)],# 1 F = 1 kg⁻¹·m⁻²·s⁴·A²
    'ohm': [('kilogram', 1, 1), ('metre',2, 1), ('second',-3, 1), ('ampere',-2, 1)],  # 1 Ω = 1 kg·m²/s³·A⁻²
    'siemens': [('kilogram',-1, 1), ('metre',-2, 1), ('second',3, 1), ('ampere',2, 1)],# 1 S = 1 kg⁻¹·m⁻²·s³·A²
    'weber': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1), ('ampere',-1, 1)],  # 1 Wb = 1 kg·m²/s²·A
    'tesla': [('kilogram', 1, 1), ('second',-2, 1), ('ampere',-1, 1)],  # 1 T = 1 kg/s²·A
    'henry': [('kilogram', 1, 1), ('metre',2, 1), ('second',-2, 1), ('ampere',-2, 1)],  # 1 H = 1 kg·m²/s²·A²
    #'degreecelsius': [('kelvin', 1, 1)], # Degree Celsius is a scale, not a unit; the unit is Kelvin
    'lumen': [('candela', 1, 1), ('steradian', 1, 1)], # 1 lm = 1 cd·sr
    'lux': [('candela', 1, 1), ('steradian', 1, 1), ('metre',-2, 1)], # 1 lx = 1 cd·sr/m²
    'becquerel': [('second',-1, 1)], # 1 Bq = 1/s
    'sievert': [('metre',2, 1), ('second',-2, 1)], # 1 Sv = 1 m²/s²
    'gray': [('metre',2, 1), ('second',-2, 1)], # 1 Gy = 1 m²/s²
    'katal': [('mole', 1, 1), ('second',-1, 1)], # 1 kat = 1 mol/s
    # Other units
    'hectare': [('metre',2, 10000)],  # 1 ha = 10000 m²
    'litre': [('metre',3, 0.001)],  # 1 L = 0.001 m³
    'tonne': [('kilogram', 1, 1000)],  # 1 t = 1000 kg
    'electronvolt': [('joule', 1, 1.602176634e-19)],  # 1 eV = 1.602176634 × 10⁻¹⁹ J
    'dalton': [('kilogram', 1, 1.66053906660e-27)],  # 1 Da = 1.66053906660 × 10⁻²⁷ kg
    'astronomicalunit': [('metre', 1, 149597870700)],  # 1 AU = 149597870700 m
    'neper': [('one', 1,1)],  # Neper is a logarithmic unit for ratios of measurements, not directly convertible
    'bel': [('one', 1,1)],  # Bel is a logarithmic unit for ratios of power, not directly convertible
    'decibel': [('one', 1,1)],  # Decibel is a logarithmic unit for ratios of power, not directly convertible

# Note: For logarithmic units like neper, bel, and decibel, conversion to base units is not straightforward due to their nature.
}
_additionalConversions = {
    # Conversions for ampere, volt, and mole into kg, s, m equivalents
    'volt': [('metre', 2, 1), ('kilogram', 1, 1), ('second', -3, 1), ('ampere', -1, 1)],  # V = kg·m²/s³·A⁻¹
    'percent':[('one',1,0.01)]
    # Note: These are placeholders and need to be adjusted to reflect accurate conversions.
}
_dsiKeyWords = {
    'tothe': r'\tothe',
    'per': r'\per'}