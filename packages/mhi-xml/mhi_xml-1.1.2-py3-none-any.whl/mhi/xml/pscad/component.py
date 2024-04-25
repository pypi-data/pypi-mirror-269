"""
XML entities for PSCAD components (this on a canvas)
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import cast, Optional, Union, TYPE_CHECKING

from mhi.xml.node import IdNode, ParamListNode

from mhi.xml.pscad.types import XY
from mhi.xml.pscad._project import project_lookup, ProjectMixin
from mhi.xml.pscad.layer import Layer


if TYPE_CHECKING:
    from mhi.xml.pscad.schematic import Schematic


#===============================================================================
# Exports
#===============================================================================


__all__ = ['Component', 'UserCmp',]


#===============================================================================
# Components
#===============================================================================

class Component(IdNode, ProjectMixin):
    """
    A Component
    """


    def __repr__(self):

        classid = self.defn or self.get('classid')
        name = self.name
        return f'{classid}[{name}, #{self.id}]'


    @property
    def classid(self) -> str:
        """
        The classid of the component.

        Typically `"UserCmp"` but other possibilities include `"WireOthogonal"`,
        `"Sticky"`, `"GraphFrame"`, `"ControlFrame"`, and so on.
        """

        classid = self.get('classid')
        assert classid is not None
        return classid


    def _ensure_id(self):

        if 'id' not in self or self.get('id') == '0':
            iid = self._file.make_id()
            self.set('id', str(iid))


    @property
    def location(self) -> XY:
        """
        The (X, Y) location of the component.
        """

        return XY(int(self.get('x', '0')), int(self.get('y', '0')))


    @location.setter
    def location(self, xy: XY) -> None:

        self.set('x', str(xy.x))
        self.set('y', str(xy.y))


    @property
    def canvas(self) -> 'Schematic':
        """
        The canvas the component is on.
        """

        return cast('Schematic', self.getparent())


    @property
    def size(self) -> XY:
        """
        The size (width & height) of the component.
        """

        return XY(int(self.get('w', '0')), int(self.get('h', '0')))


    @size.setter
    def size(self, xy: XY) -> None:

        self.set('w', str(xy.x))
        self.set('h', str(xy.y))


    @property
    def defn(self) -> Optional[str]:
        """
        The component's definition.

        .. Note:

            `None` if the component is not a `UserCmp`.
        """

        return self.get('defn')


    @property
    def scope_and_defn(self) -> tuple[str, str]:
        """
        Returns the component definitions's scope and definition names.

        .. Note:

            The "scope" is the portion before the colon (`:`).
        """

        scope = ''
        defn = self.defn or ''
        if defn:
            if ':' in defn:
                scope, defn = defn.split(':', 1)
        return scope, defn


    @property
    def name(self) -> Optional[str]:
        """
        Returns the component's assigned name value.

        The name must be stored in a parameter called `name, `Name` or `NAME`.
        """

        paramlist = self.params
        if paramlist is None:
            return None
        return next((param.get('value')
                     for param in paramlist.iter('param')
                     if param.get('name', '').casefold() == 'name'), None)


    @property
    def params(self) -> Optional[ParamListNode]:
        """
        The parameter list node of the component
        """

        xpath = 'paramlist[@link="-1"][@name=""]'
        param_list = self.find(xpath)
        if param_list is None:
            param_lists = cast(list, self.xpath('paramlist'))
            if param_lists:
                param_list = param_lists[0]

        if param_list is not None:
            return cast(ParamListNode, param_list)

        return None


    def __getitem__(self, key):

        if isinstance(key, str):
            return self.params.get_param(key)
        return super().__getitem__(key)


    def __setitem__(self, key, value):

        if isinstance(key, str):
            self.params.set_param(key, value)
        else:
            super().__setitem__(key, value)


    def __contains__(self, key) -> bool:

        if isinstance(key, str):
            if (params := self.params) is not None:
                return key in params

        return super().__contains__(key)                    # type: ignore[misc]


    def enable(self, state=True) -> None:
        """
        Enable this component

        Note:
            This does not affect whether the component is on a disabled layer.
        """

        disabled = 'false' if state else 'true'
        self.set('disable', disabled)


    def disable(self) -> None:
        """
        Disable this component
        """

        self.enable(False)


    @property
    def enabled(self) -> bool:
        """
        Is this component enabled.

        Note:
            This does not check if the component is on a disabled layer.
        """

        disabled = self.get('disable', 'false')
        return disabled.casefold() == 'false'


    @property
    def layer(self) -> Optional[Layer]:
        """
        The `Layer` the component is on, or `None` if not on any layer.
        """

        tree = self.getroottree()
        layer = tree.find(f'Layers/Layer/ref[@link="{self.id}"]/..')
        if layer is not None:
            return cast('Layer', layer)
        return None


    @layer.setter
    def layer(self, layer: Union[Layer, str, None]) -> None:

        old_layer = self.layer
        if isinstance(layer, str):
            new_layer : Optional[Layer] = self.project.layer[layer]
        else:
            new_layer = layer

        if old_layer is not None:
            if old_layer != new_layer:
                ref = old_layer.find(f'ref[@link="{self.id}"]')
                assert ref is not None
                old_layer.remove(ref)

        if new_layer is not None:
            ref = new_layer.makeelement('ref', link=str(self.id))
            new_layer.append_indented(ref, 4)


    def delete(self) -> None:
        """
        Remove this component from the canvas.
        """

        self._remove_from_parent()


#===============================================================================

@project_lookup.tag('User')
#@project_lookup.classid('UserCmp')
class UserCmp(Component):
    """
    A component with a definition defined in a '.pslx' file
    """


    XML = (
    # pylint: disable-next=line-too-long
     """<User classid="UserCmp" id="0" x="0" y="0" w="18" h="18" z="-1" orient="0" defn="{defn}" link="-1" q="4" disable="false">
          <paramlist name="" link="-1" crc="0" />
        </User>""")

    @property
    def defn(self) -> str:
        """
        The definition of the component
        """

        defn = self.get('defn')
        assert defn is not None
        return defn


    @defn.setter
    def defn(self, new_defn) -> None:

        return self.set('defn', new_defn)


    @property
    def subcanvas(self) -> Optional['Schematic']:
        """
        The component's definition's schematic, in one exists
        """

        project = self.project
        namespace, name = self.defn.split(':', 1)
        if project.namespace == namespace:
            return project.canvas(name)
        return None


    def is_module(self) -> bool:
        """
        Does this component's definition contain a schematic?
        """

        return self.subcanvas is not None


#===============================================================================

@project_lookup.tag('Wire')
#@project_lookup.classid('Branch')
#@project_lookup.classid('Bus')
#@project_lookup.classid('WireBranch')
#@project_lookup.classid('WireOrthogonal')
class Wire(Component):
    """
    Base class for all multi-vertex Wires
    """

    def vertices(self) -> list[XY]:
        """
        The XY vertices of the multi-vertex Wire
        """

        return [XY(int(vtx.get('x', '0')), int(vtx.get('y', '0')))
                for vtx in self.iterchildren('vertex')]


#===============================================================================

class TravelingWaveModelWire(Wire):
    """
    Base class for all Traveling Wave Model Wires (TLine/Cable)
    """

    @property
    def user(self) -> UserCmp:
        """
        Return the user component embedded in the Traveling Wave Model Wire
        """

        user = self.find('User')
        assert user is not None

        return cast(UserCmp, user)


    @property
    def params(self) -> ParamListNode:
        """
        Return the parameter list node for the Traveling Wave Model Wire
        """

        return cast(ParamListNode, self.user.params)


    @property
    def subcanvas(self) -> Optional['Schematic']:
        """
        Return the schematic canvas for the Traveling Wave Model Wire
        """

        namespace, name = self.user.defn.split(':', 1)

        project = self.project
        if namespace == project.namespace:
            return project.canvas(name)
        return None


#-------------------------------------------------------------------------------

@project_lookup.classid('TLine')
class TLine(TravelingWaveModelWire):
    """The PSCAD <TLine/> node class"""

    def __repr__(self) -> str:
        return f"TLine[{self.name}]"


#-------------------------------------------------------------------------------

@project_lookup.classid('Cable')
class Cable(TravelingWaveModelWire):
    """The PSCAD <Cable/> node class"""

    def __repr__(self) -> str:
        return f"Cable[{self.name}]"


#===============================================================================

@project_lookup.tag('Line')
#@project_lookup.classid('Divider')
class Line(Component):
    """The PSCAD <Line/> node class"""


#===============================================================================

@project_lookup.tag('Sticky')
#@project_lookup.classid('Sticky')
class Sticky(Component):
    """The PSCAD <Sticky/> node class"""


#===============================================================================

@project_lookup.tag('Instrument')
#@project_lookup.classid('PhasorMeter')
#@project_lookup.classid('PolyMeter')
class Instrument(Component):
    """The PSCAD <Instrument/> node class"""


#===============================================================================

@project_lookup.tag('Frame')
#@project_lookup.classid('GraphFrame')
#@project_lookup.classid('PlotFrame')
#@project_lookup.classid('ControlFrame')
class Frame(Component):
    """The PSCAD <Frame/> node class"""


#===============================================================================

@project_lookup.tag('FileCmp')
class FileCmp(Component):
    """The PSCAD <FileCmp/> node class"""
