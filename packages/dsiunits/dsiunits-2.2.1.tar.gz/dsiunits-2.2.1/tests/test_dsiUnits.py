# This file is part of dsiUnits (https://gitlab1.ptb.de/digitaldynamicmeasurement/dsiUnits/)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB)]
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import pytest
from dsiUnits import _node, _getClosestStr,dsiUnit,dsiParser
import sys
import math
from itertools import combinations
# Access the machine epsilon for the float data type
epsilon = sys.float_info.epsilon

def test_baseCase():
    # Most basic case: one unit without prefix or exponent
    tree = dsiUnit(r'\metre')
    assert tree.tree == [[_node('','metre',1.0)]]
    assert tree.toLatex() == r'$$\mathrm{m}$$'
    assert tree.valid
    assert tree.warnings == []

    # One longer unit
    tree = dsiUnit(r'\milli\metre\tothe{0.5}\kilogram\per\mega\second\tothe{3}\ampere\tothe{-2}')
    assert tree.toLatex() == r'$$\frac{\sqrt{\mathrm{m}\mathrm{m}}\,\mathrm{kg}}{\mathrm{M}\mathrm{s}^{3}\,\mathrm{A}^{-2}}$$'
    assert tree.valid
    assert tree.warnings == []


def test_robustness():
    # Unknown unit
    with pytest.warns(RuntimeWarning, match='The identifier «foo» does not match any D-SI units!'):
        tree = dsiUnit(r'\foo')
        assert tree.toLatex() == r'$${\color{red}\mathrm{foo}}$$'  
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == ['The identifier «foo» does not match any D-SI units!']
    
    # Unknown string in the middle of input
    with pytest.warns(RuntimeWarning, match=r'The identifier «mini» does not match any D-SI units! Did you mean one of these «\\milli» ?'):
        tree = dsiUnit(r'\kilo\metre\per\mini\second')
        #print(tree.toLatex())
        assert tree.toLatex() == r'$$\frac{\mathrm{k}\mathrm{m}}{{\color{red}\mathrm{mini}}\,\mathrm{s}}$$'  
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == ['The identifier «mini» does not match any D-SI units! Did you mean one of these «\\milli» ?']
    
    # Base unit missing
    with pytest.warns(RuntimeWarning, match=r'This D-SI unit seems to be missing the base unit! «\\milli\\tothe\{2\}»'):
        tree = dsiUnit(r'\milli\tothe{2}')
        #print(tree.toLatex())
        assert tree.toLatex() == r'$${\color{red}\mathrm{m}{\color{red}\mathrm{}}^{2}}$$'  
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == ['This D-SI unit seems to be missing the base unit! «\\milli\\tothe{2}»']


def test_power():
    # power
    powerTree = dsiUnit(r'\metre\tothe{2}')
    assert powerTree.tree == [[_node('','metre',2.0)]]
    assert powerTree.toLatex() == r'$$\mathrm{m}^{2}$$'
    assert powerTree.valid
    assert powerTree.warnings == []
    assert dsiUnit(r'\metre\tothe{0.5}').toLatex() == r'$$\sqrt{\mathrm{m}}$$'
    assert dsiUnit(r'\metre\tothe{-2}').toLatex() == r'$$\mathrm{m}^{-2}$$'
    assert dsiUnit(r'\metre\tothe{1337}').toLatex() == r'$$\mathrm{m}^{1337}$$'

    # Non-numerical power
    with pytest.warns(RuntimeWarning, match='The exponent «foo» is not a number!'):
        abcPowerTree = dsiUnit(r'\metre\tothe{foo}')
        assert abcPowerTree.toLatex() == r'$$\mathrm{m}^{{\color{red}\mathrm{foo}}}$$'
        assert abcPowerTree.warnings == ['The exponent «foo» is not a number!']

def test_prefix():
    # D-SI prefix
    prefixTree = dsiUnit(r'\kilo\metre')
    assert prefixTree.tree == [[_node('kilo','metre','')]]
    assert prefixTree.toLatex() == r'$$\mathrm{k}\mathrm{m}$$'
    assert prefixTree.valid

def test_node():
    # full node
    fullNodeTree = dsiUnit(r'\kilo\metre\tothe{2}')
    assert fullNodeTree.tree == [[_node('kilo','metre','2')]]
    assert fullNodeTree.toLatex() == r'$$\mathrm{k}\mathrm{m}^{2}$$'
    assert fullNodeTree.valid

def test_fraction():
    fractionTree = dsiUnit(r'\mega\metre\per\second\tothe{2}')
    assert fractionTree.tree == [[_node('mega','metre','')],[_node('','second','2')]]
    assert fractionTree.toLatex() == r'$$\frac{\mathrm{M}\mathrm{m}}{\mathrm{s}^{2}}$$'
    assert fractionTree.valid

    # double fraction
    with pytest.warns(RuntimeWarning, match=r'The dsi string contains more than one \\per, does not match specs! Given string: \\metre\\per\\metre\\per\\metre'):
        tree = dsiUnit(r'\metre\per\metre\per\metre')
        assert tree.toLatex() == r'$$\mathrm{m}{\color{red}/}\mathrm{m}{\color{red}/}\mathrm{m}$$'  
        assert not tree.valid
        assert len(tree.warnings) == 1
        assert tree.warnings == [r'The dsi string contains more than one \per, does not match specs! Given string: \metre\per\metre\per\metre']

    # empty fraction
    with pytest.warns(RuntimeWarning, match=r'The dsi string contains a \\per missing a numerator or denominator! Given string: \\per\\one'):
        tree = dsiUnit(r'\per\one')
        assert tree.toLatex() == r'$$1$$'
        assert not tree.valid
        assert len(tree.warnings) == 1

def test_empty():
    with pytest.warns(RuntimeWarning, match='Given D-SI string is empty!'):
        assert dsiUnit('').toLatex() == '$${\\color{red}\\mathrm{NULL}}$$'

def test_doubleBackslash():
    with pytest.warns(RuntimeWarning, match=r"Double backslash found in string, treating as one backslash: «\\\\metre\\per\\second»"):
        assert dsiUnit(r'\\metre\per\second').toLatex() == '$$\\frac{\\mathrm{m}}{\\mathrm{s}}$$'

def test_wrappers():
    assert dsiUnit(r'\metre').toLatex(wrapper='') == r'\mathrm{m}'
    assert dsiUnit(r'\metre').toLatex(wrapper='$', prefix=r'\mathrm{Unit: }', suffix=r'\mathrm{(generated from D-SI string)}') == r'$\mathrm{Unit: }\mathrm{m}\mathrm{(generated from D-SI string)}$'
    parserWrapper = dsiParser(latexDefaultWrapper="&")
    assert parserWrapper.parse(r'\metre').toLatex() == r'&\mathrm{m}&'
    parserFull = dsiParser(latexDefaultWrapper='@', latexDefaultPrefix=r'\mathrm{Prefix}', latexDefaultSuffix=r'\mathrm{Suffix}')
    assert parserFull.parse(r'\metre').toLatex() == r'@\mathrm{Prefix}\mathrm{m}\mathrm{Suffix}@'

def test_getClosestMatch():
    closestMatch = _getClosestStr('\kiilo')
    assert closestMatch == (['kilo'])
    closestMatch = _getClosestStr('\mettre')
    assert closestMatch == (['metre'])
    closestMatch = _getClosestStr(r'\ttothe')
    assert closestMatch == (['tothe'])

def test_info():
    p=dsiParser()
    infoStr, dsiVersion, dsiSchemaUrl, dsiRepositoryURL =p.info()
    #assert infoStr == "D-SI Parser Version: "+ str(dsiParser)+ "using D-SI Schema Version: "+ str(dsiParser._dsiParser__dsiVersion)+ "from: "+ str(dsiParser._dsiParser__dsiRepositoryURL)+ "using D-SI Schema: "+ str(dsiParser._dsiParser__dsiSchemaUrl)
    assert dsiVersion == dsiParser._dsiParser__dsiVersion
    assert dsiSchemaUrl == dsiParser._dsiParser__dsiSchemaUrl
    assert dsiRepositoryURL == dsiParser._dsiParser__dsiRepositoryURL

def test_fractionalPowers():
    assert dsiUnit(r'\metre\tothe{0.3333333333333333333}').toLatex(wrapper='') == r'\mathrm{m}\sqrt[3]{\mathrm{m}}'
    assert dsiUnit(r'\metre\tothe{0.666666666666666}').toLatex(wrapper='') == r'\mathrm{m}\sqrt[3]{\mathrm{m}^{2}}'

def test_baseUnitConversion():
    # Test conversion of a single derived unit to its base unit
    derivedUnitTree = dsiUnit(r'\kilo\metre')
    baseUnitTree = derivedUnitTree.toBaseUnitTree()
    assert baseUnitTree.tree == [[_node('', 'metre', '', 1000)]]
    assert baseUnitTree.toLatex() == '$$\\mathrm{m}$$'

    # Test conversion of a complex unit with a fraction to base units
    complexUnitTree = dsiUnit(r'\kilo\watt\hour')
    complexUnitTree2 = dsiUnit(r'\kilo\watt\hour')
    complexBaseUnitTree = complexUnitTree.toBaseUnitTree()
    reduceFractionTree = complexBaseUnitTree.reduceFraction()
    megacomplexUnitTree = dsiUnit(r'\mega\watt\hour')
    voltAmpereSeconds = dsiUnit(r'\volt\ampere\second')
    assert (complexUnitTree == complexUnitTree2) == True
    assert (complexUnitTree == 'Sting') == False
    scalFactor, commonBaseUnit=complexUnitTree.isScalablyEqualTo('Sting')
    assert math.isnan(scalFactor)
    assert commonBaseUnit == None
    assert (complexBaseUnitTree == megacomplexUnitTree) == False
    assert (megacomplexUnitTree == voltAmpereSeconds) == False
    kmh = dsiUnit(r'\kilo\metre\per\hour')
    ms = dsiUnit(r'\metre\per\second')
    scalFactor, commonBaseUnit = kmh.isScalablyEqualTo(ms)
    assert scalFactor-3.6<epsilon
    assert commonBaseUnit.toLatex() == '$$\\mathrm{m}\\,\\mathrm{s}^{-1}$$'
    ohmUnitTree = dsiUnit(r'\ohm')
    otherOhmesList = [
    dsiUnit(r'\siemens\tothe{-1}'),
    dsiUnit(r'\volt\per\ampere'),
    dsiUnit(r'\watt\ampere\tothe{-2}'),
    dsiUnit(r'\second\per\farad'),
    dsiUnit(r'\weber\per\coulomb'),
    dsiUnit(r'\volt\per\ampere'),
    dsiUnit(r'\siemens\tothe{-1}'),
    dsiUnit(r'\watt\per\ampere\tothe{2}'),
    dsiUnit(r'\volt\tothe{2}\per\watt'),
    dsiUnit(r'\second\per\farad'),
    dsiUnit(r'\henry\per\second'),
    dsiUnit(r'\weber\per\coulomb'),
    dsiUnit(r'\weber\coulomb\tothe{-1}'),
    dsiUnit(r'\joule\second\per\coulomb\tothe{2}'),
    dsiUnit(r'\kilogram\metre\tothe{2}\per\second\coulomb\tothe{2}'),
    dsiUnit(r'\joule\per\second\ampere\tothe{2}'),
    dsiUnit(r'\kilogram\metre\tothe{2}\per\second\tothe{3}\ampere\tothe{2}')]
    for otherOhm in otherOhmesList:
        try:
            scalFactor, commonBaseUnit = ohmUnitTree.isScalablyEqualTo(otherOhm)
        except Exception as E:
            print(E+"WAAAAAAAAAAAAAAAAAAA")
        assert scalFactor-1<epsilon
        assert commonBaseUnit.toLatex() == '$$\\mathrm{A}^{-2}\\,\\mathrm{kg}\\,\\mathrm{m}^{2}\\,\\mathrm{s}^{-3}$$'

def test_perAndToTheNegComp():
    kmhs=(dsiUnit(r"\kilo\metre\hour\tothe{-1}"),dsiUnit(r"\kilo\metre\per\hour"))
    mss=(dsiUnit(r"\metre\second\tothe{-1}"),dsiUnit(r"\metre\per\second"))
    scalfactorsKMH=[]
    baseUnitsKMH=[]
    # kmh to ms
    for i in range(2):
        for j in range(2):
            scalfactor,baseunit=kmhs[i].isScalablyEqualTo(mss[j])
            scalfactorsKMH.append(scalfactor)
            baseUnitsKMH.append(baseunit)
    assert all(x==scalfactorsKMH[0] for x in scalfactorsKMH)
    assert all(x == baseUnitsKMH[0] for x in baseUnitsKMH)
    # ms to kmh
    scalfactorsMS=[]
    baseUnitsMS=[]
    for i in range(2):
        for j in range(2):
            scalfactor,baseunit=mss[i].isScalablyEqualTo(kmhs[j])
            scalfactorsMS.append(scalfactor)
            baseUnitsMS.append(baseunit)
    assert all(x==scalfactorsMS[0] for x in scalfactorsMS)
    assert all(x == baseUnitsMS[0] for x in baseUnitsMS)
    assert scalfactorsMS[0]-(1.0/scalfactorsKMH[0])<epsilon

def test_str():
    assert str(dsiUnit(r'\metre')) == r'\metre'
    assert str(dsiUnit(r'\metre\tothe{2}')) == r'\metre\tothe{2}'
    assert str(dsiUnit(r'\kilo\metre\tothe{2}')) == r'\kilo\metre\tothe{2}'
    assert str(dsiUnit(r'\kilo\metre\tothe{-2}')) == r'\kilo\metre\tothe{-2}'
    assert str(dsiUnit(r'\kilo\metre\tothe{0.5}')) == r'\kilo\metre\tothe{0.5}'
    assert str(dsiUnit(r'\kilo\metre\tothe{0.333333333333333}')) == r'\kilo\metre\tothe{0.333333}'
    assert str(dsiUnit(r'\kilo\metre\tothe{0.666666666666666}')) == r'\kilo\metre\tothe{0.666667}'
    assert str(dsiUnit(r'\kilo\metre\tothe{1337}')) == r'\kilo\metre\tothe{1337}'
    assert str(dsiUnit(r'\kilo\metre\tothe{2}\per\volt')) == r'\kilo\metre\tothe{2}\per\volt'

def test_complete():
    # Test 1: Volt-Ampere to Watt conversion
    VA = dsiUnit(r"\volt\ampere")
    Watt = dsiUnit(r"\watt")
    scaleFactor, commonBaseUnit = VA.isScalablyEqualTo(Watt, complete=True)
    assert abs(scaleFactor - 1.0) < epsilon, "Scale factor for VA to Watt should be 1.0"
    assert commonBaseUnit.toLatex() == '$$\\mathrm{kg}\\,\\mathrm{m}^{2}\\,\\mathrm{s}^{-3}$$', "Base unit representation for power should be in kg, m^2, s^-3"

    # Expanded Test Cases for Other Units of Power Equal to Watt
    units_of_power = [
        r"\volt\tothe{2}\per\ohm",  # Volt squared per ohm
        r"\ampere\tothe{2}\ohm",  # Ampere squared times ohm
        r"\volt\ampere",  # Volt times ampere (directly equivalent to watt)
        r"\kilogram\metre\tothe{2}\per\second\tothe{3}",  # kg m^2 / s^3, directly equivalent to watt
        r"\joule\per\second",  # Directly equivalent to watt
        r"\newton\metre\per\second",  # Newton metre per second
        r"\pascal\metre\tothe{3}\per\second",  # Pascal times cubic meter per second
        r"\coulomb\volt\per\second",  # Coulomb times volt per second
        r"\farad\volt\tothe{2}\per\second",  # Farad times volt squared per second
        r"\henry\ampere\tothe{2}\per\second",  # Henry times ampere squared per second
        r"\weber\ampere\per\second",  # Weber times ampere per second
        # Equivalent through direct and indirect relationships
        # Test cases involving inverse units
        r"\siemens\volt\tothe{2}"
    ]

    # Verify each unit of power is scalably equal to Watt with complete base unit conversion
    for unit_str in units_of_power:
        otherUnit = dsiUnit(unit_str)
        scaleFactor, _ = otherUnit.isScalablyEqualTo(Watt, complete=True)
        assert abs(scaleFactor - 1.0) < epsilon, f"Scale factor for {unit_str} to Watt should be 1.0"
        assert commonBaseUnit.toLatex() == '$$\\mathrm{kg}\\,\\mathrm{m}^{2}\\,\\mathrm{s}^{-3}$$', f"Base unit representation for {unit_str} should be in kg, m^2, s^-3"

def test_toUTF8():
    units_of_power = [
        (r"\volt\tothe{2}\per\ohm", "V²/Ω"),
        (r"\ampere\tothe{2}\ohm", "A²Ω"),
        (r"\volt\ampere", "VA"),
        (r"\kilogram\metre\tothe{2}\per\second\tothe{3}", "kgm²/s³"),
        (r"\joule\per\second", "J/s"),
        (r"\newton\metre\per\second", "Nm/s"),
        (r"\pascal\metre\tothe{3}\per\second", "Pam³/s"),
        (r"\coulomb\volt\per\second", "CV/s"),
        (r"\farad\volt\tothe{2}\per\second", "FV²/s"),
        (r"\henry\ampere\tothe{2}\per\second", "HA²/s"),
        (r"\weber\ampere\per\second", "WbA/s"),
        (r"\siemens\volt\tothe{2}", "SV²"),
    ]

    for unit_input, expected_output in units_of_power:
        dsiTree = dsiUnit(unit_input)
        utf8_output = dsiTree.toUTF8()
        assert utf8_output == expected_output, f"Expected {expected_output}, got {utf8_output}"

def test_fromAscii():
    test_cases = [
        # Compact form without spaces
        # Form using ^ for exponents
        ("A^2Ω", r"\ampere\tothe{2}\ohm"),
        # Handling fractions
        ("J/s", r"\joule\per\second"),
        # More complex examples
        ("WbA/s", r"\weber\ampere\per\second"),
        ("Pam³/s", r"\pascal\metre\tothe{3}\per\second"),
        # Nested exponents and fractions
        ("FV^2/s", r"\farad\volt\tothe{2}\per\second"),
        # Negative exponents
        ("m/s^2", r"\metre\per\second\tothe{2}"),
        # Multiple units without explicit multiplication sign
        ("kgm/s^2", r"\kilogram\metre\per\second\tothe{2}"),
        ("kgm²/s³", r"\kilogram\metre\tothe{2}\per\second\tothe{3}"),
    ]

def test_percent():
    percentDsiTree=dsiUnit(r'\percent')
    assert percentDsiTree.toUTF8()=='%'
    oneDsiTree=dsiUnit(r'\one')
    normalCompresult=percentDsiTree.isScalablyEqualTo(oneDsiTree, complete=False)
    assert math.isnan(normalCompresult[0])
    completeComparison=percentDsiTree.isScalablyEqualTo(oneDsiTree, complete=True)
    assert completeComparison[0]==100 #TODO double check if this is 100 or 0.01
    assert completeComparison[1].toUTF8()=='1'

def test_multiplication():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    V=dsiUnit(r'\volt')
    A=dsiUnit(r'\ampere')
    ms=dsiUnit(r'\metre\second')
    mps=dsiUnit(r'\metre\per\second')
    multiplyed=m*s
    multiplyedmmps=m*mps
    multiplyedmpss = mps*s
    assert multiplyed==ms
    assert multiplyedmpss==m
    assert dsiUnit('\\metre\\tothe{2}\\second\\tothe{-1}')==multiplyedmmps

def test_division():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    ms=dsiUnit(r'\metre\second')
    mps=dsiUnit(r'\metre\per\second')
    divideed=ms/s
    divideedmps=mps/s
    divideedmpss = ms/mps
    assert divideed==m
    assert divideedmpss==s**2
    assert divideedmps==dsiUnit(r'\metre\second\tothe{-2}')

def test_power():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    ms=dsiUnit(r'\metre\second')
    mps=dsiUnit(r'\metre\per\second')
    powered=m**2
    poweredmps=mps**2
    poweredmpss = ms**2
    assert powered==dsiUnit(r'\metre\tothe{2}')
    assert poweredmps.isScalablyEqualTo(dsiUnit(r'\metre\tothe{2}\per\second\tothe{2}'))[0]==1.0
    assert poweredmpss==dsiUnit(r'\metre\tothe{2}\second\tothe{2}')

def test_ComparisonOfperandNotPer():
    m=dsiUnit(r'\metre')
    s=dsiUnit(r'\second')
    mps=dsiUnit(r'\metre\per\second')
    mpsfromDiv=m/s
    assert mps.isScalablyEqualTo(m/s)[0]==1.0
    assert mps.isScalablyEqualTo(m/s,complete=True)[0]==1.0
    assert mps==mpsfromDiv


def test_ifOnlyScaled():
    V=dsiUnit(r'\volt')
    mV = dsiUnit(r'\milli\volt')
    assert (V==mV)==False
    assert mV.isScalablyEqualTo(V)[0]==1000,dsiUnit(r'\volt')
    min=dsiUnit(r'\minute')
    s = dsiUnit(r'\second')
    assert (min==s)==False
    assert s.isScalablyEqualTo(min)[0]==60,dsiUnit(r'\second')