#-*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| File contributors :                                                       |
#|       - Georges Bossert <georges.bossert (a) supelec.fr>                  |
#|       - Frédéric Guihéry <frederic.guihery (a) amossys.fr>                |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Standard library imports                                                  |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Related third party imports                                               |
#+---------------------------------------------------------------------------+

#+---------------------------------------------------------------------------+
#| Local application imports                                                 |
#+---------------------------------------------------------------------------+
from netzob.Common.Utils.Decorators import typeCheck
from netzob.Common.Models.Vocabulary.AbstractField import AbstractField
from netzob.Common.Models.Types.AbstractType import AbstractType
from netzob.Inference.Vocabulary.FormatEditorOperations.FieldSplitStatic.FieldSplitStatic import FieldSplitStatic
from netzob.Inference.Vocabulary.FormatEditorOperations.FieldReseter import FieldReseter
from netzob.Common.Models.Vocabulary.Symbol import Symbol


class FormatEditor(object):
    """This class is a wrapper for all the various tools
    which allow to edit the format of a field.

    """

    @staticmethod
    @typeCheck(AbstractField, str)
    def splitStatic(field, unitSize=AbstractType.UNITSIZE_8, mergeAdjacentStaticFields=True, mergeAdjacentDynamicFields=True):
        """Split the portion of the message matching the specified fields
        following their variations of each unitsize.
        This method returns nothing, it upgrades the field structure
        with the result of the splitting process.

        Its a wrapper for :class:`netzob.Inference.Vocabulary.FieldSplitStatic.ParallelFieldSplitStatic.ParallelFieldSplitStatic`.


        >>> import binascii
        >>> from netzob.all import *
        >>> samples = ["00ff2f000000",	"000010000000",	"00fe1f000000",	"000020000000", "00ff1f000000",	"00ff1f000000",	"00ff2f000000",	"00fe1f000000"]
        >>> messages = [RawMessage(data=binascii.unhexlify(sample)) for sample in samples]
        >>> symbol = Symbol(messages=messages)
        >>> print symbol
        00ff2f000000
        000010000000
        00fe1f000000
        000020000000
        00ff1f000000
        00ff1f000000
        00ff2f000000
        00fe1f000000
        >>> FormatEditor.splitStatic(symbol)
        >>> print symbol
        00 | ff2f | 000000
        00 | 0010 | 000000
        00 | fe1f | 000000
        00 | 0020 | 000000
        00 | ff1f | 000000
        00 | ff1f | 000000
        00 | ff2f | 000000
        00 | fe1f | 000000

        :param field: the field for which we update the format
        :type field: :class:`netzob.Common.Models.Vocabulary.AbstractField.AbstractField`
        :keyword unitSize: the required size of static element to create a static field
        :type unitSize: :class:`int`.
        :keyword mergeAdjacentStaticFields: if set to true, adjacent static fields are merged in a single field
        :type mergeAdjacentStaticFields: :class:`bool`
        :keyword mergeAdjacentDynamicFields: if set to true, adjacent dynamic fields are merged in a single field
        :type mergeAdjacentDynamicFields: :class:`bool`
        :raise Exception if something bad happens
        """

        if field is None:
            raise TypeError("Field cannot be None")

        if unitSize is None:
            raise TypeError("Unitsize cannot be None")

        FieldSplitStatic.split(field, unitSize, mergeAdjacentStaticFields, mergeAdjacentDynamicFields)

    @staticmethod
    @typeCheck(AbstractField)
    def resetFormat(field):
        """Reset the format (field hierarchy and definition domain) of
        the specified field.

        >>> import binascii
        >>> from netzob.all import *
        >>> samples = ["00ff2f000000",	"000010000000",	"00fe1f000000"]
        >>> messages = [RawMessage(data=binascii.unhexlify(sample)) for sample in samples]
        >>> f1 = Field(Raw(size=(1)))
        >>> f2 = Field(Raw(size=(2)))
        >>> f3 = Field(Raw(size=(3)))
        >>> symbol = Symbol([f1, f2, f3], messages=messages)
        >>> print symbol
        00 | ff2f | 000000
        00 | 0010 | 000000
        00 | fe1f | 000000
        >>> FormatEditor.resetFormat(symbol)
        >>> print symbol
        00ff2f000000
        000010000000
        00fe1f000000

        :param field: the field we want to reset
        :type field: :class:`netzob.Common.Models.Vocabulary.AbstractField.AbstractField`
        :raise Exception if something bad happens
        """
        if field is None:
            raise TypeError("The field to reset must be specified and cannot be None")

        fr = FieldReseter()
        fr.reset(field)