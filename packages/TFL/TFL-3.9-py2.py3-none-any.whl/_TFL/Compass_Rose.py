# -*- coding: utf-8 -*-
# Copyright (C) 2024 Christian Tanzer All rights reserved
# tanzer@gg32.com.
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    Compass_Rose
#
# Purpose
#    Model a compass rose with 4, 8, or 16 points
#
# Revision Dates
#    13-Apr-2024 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                       import TFL

from   _TFL.Angle                 import Angle_D
from   _TFL.predicate             import rounded_down, rounded_to
from   _TFL._Meta.Property        import Alias_Property
from   _TFL._Meta.Once_Property   import Once_Property

import _TFL._Meta.Object

class _Direction_ (Angle_D) :
    """Model a point direction in a compass rose.

    >>> for a in range (0, 360, 45) :
    ...   d16 = Compass_Rose.p16.Direction (a)
    ...   print ("%r, %s" % (d16, d16.range_str))
    N   [  0.0, raw =   0], [-11.25°,  11.25°)
    NE  [ 45.0, raw =  45], [ 33.75°,  56.25°)
    E   [ 90.0, raw =  90], [ 78.75°, 101.25°)
    SE  [135.0, raw = 135], [123.75°, 146.25°)
    S   [180.0, raw = 180], [168.75°, 191.25°)
    SW  [225.0, raw = 225], [213.75°, 236.25°)
    W   [270.0, raw = 270], [258.75°, 281.25°)
    NW  [315.0, raw = 315], [303.75°, 326.25°)

    >>> for a in range (30, 360, 45) :
    ...   d16 = Compass_Rose.p16.Direction (a)
    ...   print ("%r, %s" % (d16, d16.range_str))
    NNE [ 22.5, raw =  30], [ 11.25°,  33.75°)
    ENE [ 67.5, raw =  75], [ 56.25°,  78.75°)
    ESE [112.5, raw = 120], [101.25°, 123.75°)
    SSE [157.5, raw = 165], [146.25°, 168.75°)
    SSW [202.5, raw = 210], [191.25°, 213.75°)
    WSW [247.5, raw = 255], [236.25°, 258.75°)
    WNW [292.5, raw = 300], [281.25°, 303.75°)
    NNW [337.5, raw = 345], [326.25°, 348.75°)

    >>> for a in range (30, 360, 45) :
    ...   Compass_Rose.p4.Direction (a)
    N   [  0.0, raw =  30]
    E   [ 90.0, raw =  75]
    E   [ 90.0, raw = 120]
    S   [180.0, raw = 165]
    S   [180.0, raw = 210]
    W   [270.0, raw = 255]
    W   [270.0, raw = 300]
    N   [  0.0, raw = 345]

    >>> for a in (44, 45, 46, 134, 135, 136, 224, 225, 226, 314, 315, 316) :
    ...   Compass_Rose.p4.Direction (a)
    N   [  0.0, raw =  44]
    E   [ 90.0, raw =  45]
    E   [ 90.0, raw =  46]
    E   [ 90.0, raw = 134]
    S   [180.0, raw = 135]
    S   [180.0, raw = 136]
    S   [180.0, raw = 224]
    W   [270.0, raw = 225]
    W   [270.0, raw = 226]
    W   [270.0, raw = 314]
    N   [  0.0, raw = 315]
    N   [  0.0, raw = 316]

    >>> for a in range (30, 360, 45) :
    ...   Compass_Rose.p4_ordinal.Direction  (a)
    NE  [ 45.0, raw =  30]
    NE  [ 45.0, raw =  75]
    SE  [135.0, raw = 120]
    SE  [135.0, raw = 165]
    SW  [225.0, raw = 210]
    SW  [225.0, raw = 255]
    NW  [315.0, raw = 300]
    NW  [315.0, raw = 345]

    >>> for a in (0, 1, 89, 90, 91, 179, 180, 181, 269, 270, 271, 359) :
    ...   Compass_Rose.p4_ordinal.Direction  (a)
    NE  [ 45.0, raw =   0]
    NE  [ 45.0, raw =   1]
    NE  [ 45.0, raw =  89]
    SE  [135.0, raw =  90]
    SE  [135.0, raw =  91]
    SE  [135.0, raw = 179]
    SW  [225.0, raw = 180]
    SW  [225.0, raw = 181]
    SW  [225.0, raw = 269]
    NW  [315.0, raw = 270]
    NW  [315.0, raw = 271]
    NW  [315.0, raw = 359]

    >>> cr4 = Compass_Rose.p4
    >>> ans = [cr4.Direction (a) for a in range (5, 75, 10)]
    >>> for a in ans :
    ...   print (repr (a))
    N   [  0.0, raw =   5]
    N   [  0.0, raw =  15]
    N   [  0.0, raw =  25]
    N   [  0.0, raw =  35]
    E   [ 90.0, raw =  45]
    E   [ 90.0, raw =  55]
    E   [ 90.0, raw =  65]

    >>> sum (ans, cr4.Zero) / len (ans)
    N   [  0.0, raw =  35]

    >>> aes = [cr4.Direction (a) for a in range (15, 85, 10)]
    >>> for a in aes :
    ...   print (repr (a))
    N   [  0.0, raw =  15]
    N   [  0.0, raw =  25]
    N   [  0.0, raw =  35]
    E   [ 90.0, raw =  45]
    E   [ 90.0, raw =  55]
    E   [ 90.0, raw =  65]
    E   [ 90.0, raw =  75]

    >>> sum (aes, cr4.Zero) / len (aes)
    E   [ 90.0, raw =  45]

    >>> cro = Compass_Rose.p4_ordinal
    >>> aos = [cro.Direction (a) for a in range (35, -45, -10)]
    >>> for a in aos :
    ...   print (repr (a), float (a))
    NE  [ 45.0, raw =  35] 35.0
    NE  [ 45.0, raw =  25] 25.0
    NE  [ 45.0, raw =  15] 15.0
    NE  [ 45.0, raw =   5] 5.0
    NW  [315.0, raw =  -5] -5.0
    NW  [315.0, raw = -15] -15.0
    NW  [315.0, raw = -25] -25.0
    NW  [315.0, raw = -35] -35.0

    >>> sum (aos, cro.Zero) / len (aos)
    NE  [ 45.0, raw =   0]

    """

    compass_rose    = None
    CR              = Alias_Property ("compass_rose")

    index           = Alias_Property ("sector")
    raw_az          = Alias_Property ("degrees")

    @property
    def angle (self) :
        """Name of point associated to this direction in compass rose."""
        return self.compass_rose.point_to_angle [self.point]
    # end def point

    @Once_Property
    def point (self) :
        return self.compass_rose.points [self.sector]
    # end def point

    @Once_Property
    def range (self) :
        a   = self.angle
        dh  = self.compass_rose.angle_dh
        return (a - dh, a + dh)
    # end def range

    @property
    def range_str (self) :
        return "[%6.2f°, %6.2f°)" % self.range
    # end def range_str

    @Once_Property
    def sector (self) :
        az  = self.raw_az
        cr  = self.compass_rose
        return int (((az + cr.angle_dh - cr.angle_b) % 360) // cr.angle_d)
    # end def sector

    def __repr__ (self) :
        return "%-3s [%5.1f, raw = %3g]" % \
            (self.point, self.angle, self.raw_az)
    # end def __repr__

    def __str__ (self) :
        return self.point
    # end def __str__

# end class _Direction_

class M_Compass_Rose (TFL.Meta.Object.__class__) :
    """Meta class for `Compass_Rose` caching instances, providing shorthands."""

    def __call__ (cls, np, bias = 0) :
        try :
            result = cls.Table [(np, bias)]
        except KeyError :
            result = cls.Table [(np, bias)] = super ().__call__ (np, bias)
        return result
    # end def __call__

    @property
    def p4 (self) :
        """Compass_Rose with 4 points."""
        return Compass_Rose (4)
    # end def p4

    @property
    def p4_ordinal (self) :
        """Compass_Rose with 4 ordinal points (NE, SE, SW, NW)."""
        return Compass_Rose (4, bias = 2)
    # end def p16

    @property
    def p8 (self) :
        """Compass_Rose with 8 points."""
        return Compass_Rose (8)
    # end def p8

    @property
    def p16 (self) :
        """Compass_Rose with 16 points."""
        return Compass_Rose (16)
    # end def p16

# end class M_Compass_Rose

class Compass_Rose (TFL.Meta.Object, metaclass = M_Compass_Rose) :
    """Base class for compass roses.

    >>> Compass_Rose.p4
    Compass_Rose: N/E/S/W

    >>> Compass_Rose.p4_ordinal
    Compass_Rose: NE/SE/SW/NW

    >>> Compass_Rose.p8
    Compass_Rose: N/NE/E/SE/S/SW/W/NW

    >>> Compass_Rose.p16
    Compass_Rose: N/NNE/NE/ENE/E/ESE/SE/SSE/S/SSW/SW/WSW/W/WNW/NW/NNW

    >>> for b in range (0, 4) :
    ...   print ("%2d : %s" % (b, Compass_Rose (4, bias = b)))
     0 : Compass_Rose: N/E/S/W
     1 : Compass_Rose: NNE/ESE/SSW/WNW
     2 : Compass_Rose: NE/SE/SW/NW
     3 : Compass_Rose: ENE/SSE/WSW/NNW

    >>> for b in range (0, 2) :
    ...   print ("%2d : %s" % (b, Compass_Rose (8, bias = b)))
     0 : Compass_Rose: N/NE/E/SE/S/SW/W/NW
     1 : Compass_Rose: NNE/ENE/ESE/SSE/SSW/WSW/WNW/NNW

    >>> with expect_except (ValueError) :
    ...   Compass_Rose (5)
    ValueError: Number of points must be one of 2, 4, 8, 16; got 5

    >>> with expect_except (ValueError) :
    ...   Compass_Rose (4, bias = 4)
    ValueError: Bias must be <3.0; got 4

    >>> Compass_Rose.p4 is Compass_Rose (4)
    True

    >>> Compass_Rose.p4 is Compass_Rose (4, bias = 2)
    False

    >>> Compass_Rose.p4_ordinal is Compass_Rose (4, bias = 2)
    True

    >>> for cr in Compass_Rose.p4, Compass_Rose.p4_ordinal, Compass_Rose.p8, Compass_Rose.p16:
    ...   print ("%2d %d, %4.1f, %4.1f, %4.1f " % (cr.np, cr.bias, cr.angle_d, cr.angle_dh, cr.angle_b))
     4 0, 90.0, 45.0,  0.0
     4 2, 90.0, 45.0, 45.0
     8 0, 45.0, 22.5,  0.0
    16 0, 22.5, 11.2,  0.0

    """

    Table               = {}

    points_16           = \
        ( "N", "NNE", "NE", "ENE"
        , "E", "ESE", "SE", "SSE"
        , "S", "SSW", "SW", "WSW"
        , "W", "WNW", "NW", "NNW"
        )

    point_to_angle      = { p : 22.5 * i for i, p in enumerate (points_16)   }
    angle_to_point      = { a : p        for p, a in point_to_angle.items () }

    def __init__ (self, np, bias = 0) :
        if np not in (2, 4, 8, 16) :
            raise ValueError \
                ("Number of points must be one of 2, 4, 8, 16; got %s" % np)
        if bias > (max_bias := (16 / np - 1)) :
            raise ValueError ("Bias must be <%s; got %s" % (max_bias, bias))
        self.np         = np
        self.bias       = bias
        self.angle_d    = ad = 360 / np
        self.angle_dh   = ad / 2
        self.angle_b    = (360 / 16) * bias
        self.points     = self.points_16 [bias::16//np]
        self.Direction  = _Direction_.New \
            ("_%d__%d" % (np, bias), compass_rose = self)
    # end def __init__

    @Once_Property
    def Zero (self) :
        return self.Direction (0)
    # end def Zero

    def __repr__ (self) :
        return "Compass_Rose: %s" % ("/".join (self.points))
    # end def __repr__

# end class Compass_Rose

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Compass_Rose
