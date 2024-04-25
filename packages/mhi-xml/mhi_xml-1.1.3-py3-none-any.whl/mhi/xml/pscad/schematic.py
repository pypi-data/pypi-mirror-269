"""
XML entities for PSCAD schematics
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from typing import cast, Iterator, Optional, TYPE_CHECKING

from mhi.xml.node import XmlNode, ParametersBase, ParamListNode
from mhi.xml.pscad._project import project_lookup, ProjectMixin

from mhi.xml.pscad.types import XY
from mhi.xml.pscad.component import Component, UserCmp

if TYPE_CHECKING:
    from mhi.xml.pscad.definition import Definition


#===============================================================================
# Exports
#===============================================================================

__all__ = ['Schematic', ]


#===============================================================================
# Schematic Canvases
#===============================================================================

@project_lookup.tag('schematic')
class Schematic(XmlNode, ProjectMixin):
    """
    A canvas which contains a set of components.
    """

    @staticmethod
    def _xpath(xpath: Optional[str],
               classid: Optional[str],
               defn: Optional[str],
               with_params: Optional[set[str]],
               params: Optional[dict[str, str]]
               ) -> str:

        if xpath:
            if classid or defn or with_params or params:
                raise ValueError(
                    f"xpath cannot be used with classid/defn/params\n"
                    f"    xpath={xpath}\n"
                    f"    classid={classid}\n"
                    f"    defn={defn}\n"
                    f"    with_params={with_params}\n"
                    f"    params={params}")
            return xpath

        parts = []
        node = "*"
        if classid is not None:
            node += f"[@classid={classid!r}]" if classid else "[@classid]"
        if defn:
            node += f"[@defn={defn!r}]"
        parts.append(node)

        if params or with_params:
            parts.append('paramlist')
            if params:
                parts.extend(f"param[@name={name!r}][@value={value!r}]/.."
                             for name, value in params.items())
            if with_params:
                if params:
                    with_params = with_params - params.keys()
                parts.extend(f"param[@name={name!r}]/.."
                             for name in with_params)
            parts.append("..")

        xpath = "/".join(parts)

        return xpath


    def __repr__(self):

        classid = self.get('classid', 'Unknown!')
        return f'{classid}[{self.name!r}]'


    def __iter__(self):

        yield from self.xpath("*[@classid]")


    def __getitem__(self, key):

        xpath = ""
        if isinstance(key, int):
            xpath = f"*[@id='{key}']"
        else:
            raise KeyError(f"Invalid schematic component key={key!r}")

        return self.find(xpath)


    @property
    def name(self) -> str:
        """
        Name of the schematic's definition
        """

        return self.definition.name


    @property
    def definition(self) -> 'Definition':
        """
        Definition the schematic is part of
        """

        return cast('Definition', self.getparent())


    def components(self,                    # pylint: disable=too-many-arguments
                   name: Optional[str] = None, /, *,
                   defn: Optional[str] = None,
                   include_defns: Optional[set[str]] = None,
                   exclude_defns: Optional[set[str]] = None,
                   xpath: Optional[str] = None,
                   classid: Optional[str] = None,
                   with_params: Optional[set[str]] = None,
                   **params) -> Iterator[Component]:
        """
        Component search

        Find the components within the canvas identified by the provided
        arguments.  All arguments are optional.  The name parameter, if
        given, must be the first and only positional parameter.  All other
        parameters must be keyword parameters.

        :param str name: Name of the component (positional parameter only)
        :param str classid: Component class identifier
        :param str defn: Definition name
        :param set[str] include_defns: Definition names to include in search
        :param set[str] exclude_defns: Definition names to exclude from search
        :param set[str] with_params: Only components with have the given parameters
        :param key=value: Components with the given parameter key=value pairs

        At most one of `defn`, `include_defns` or `exclude_defns` may be
        provided.
        """

        xpath = self._xpath(xpath, classid, defn, with_params, params)

        if name:
            name = name.casefold()

        cmps = cast(list[Component], self.xpath(xpath))
        for cmp in cmps:
            if cmp.tag in {'paramlist', 'grouping'}:
                continue
            if name is not None:
                cmp_name = cmp.name
                if cmp_name is None or cmp_name.casefold() != name:
                    continue
            if include_defns and cmp.defn not in include_defns:
                continue
            if exclude_defns and cmp.defn in exclude_defns:
                continue
            yield cmp


    def component(self,                     # pylint: disable=too-many-arguments
                  name: Optional[str] = None, /, *,
                  defn: Optional[str] = None,
                  include_defns: Optional[set[str]] = None,
                  exclude_defns: Optional[set[str]] = None,
                  xpath: Optional[str] = None,
                  raise_if_not_found: bool = False,
                  classid: Optional[str] = None,
                  with_params: Optional[set[str]] = None,
                  **params) -> Optional[Component]:
        """
        Component search

        Find the component within the canas identified by the provided
        arguments.  All arguments are optional.  The name parameter, if
        given, must be the first and only positional parameter.  All
        other parameters must be keyword parameters.

        :param str name: Name of the component (positional parameter only)
        :param str classid: Component class identifier
        :param str defn: Definition name
        :param set[str] include_defns: Definition names to include in search
        :param set[str] exclude_defns: Definition names to exclude from search
        :param bool raise_if_not_found: Raise an exception if component isn't found (default: False)
        :param set[str] with_params: Only components with have the given parameters
        :param key=value: Components with the given parameter key=value pairs

        At most one of `defn`, `include_defns` or `exclude_defns` may be
        provided.
        """

        xpath = self._xpath(xpath, classid, defn, with_params, params)
        comps = list(self.components(name, xpath=xpath,
                                     include_defns=include_defns,
                                     exclude_defns=exclude_defns))

        if len(comps) == 0:
            if raise_if_not_found:
                raise NameError(f"Component {xpath!r} not found")
            return None
        if len(comps) > 1:
            raise NameError(f"Multiple components {xpath!r} found ({len(comps)})")

        return comps[0]


    def page_modules(self) -> Iterator[UserCmp]:
        """
        Retrieve the page module components on the canvas
        """

        project = self.project
        project_namespace = project.namespace
        for user in self.iterfind('User[@classid="UserCmp"]'):
            user = cast(UserCmp, user)
            namespace, name = user.defn.split(':', 1)
            if namespace == project_namespace:
                canvas = project.canvas(name)
                if canvas is not None:
                    yield user

    def remove_components(self, component, *components) -> None:
        """
        Remove listed components from the schematic
        """

        self.remove(component)

        for cmp in components:
            self.remove(cmp)


    def remove(self, component) -> None:
        """
        Remove the given components from the schematic
        """

        iid = component.id
        super().remove(component)
        if iid:
            refs = cast(list[XmlNode],
                        self.xpath(f'/Layers/Layer/ref[@id="{iid}"]'))
            for ref in refs:
                ref._remove_from_parent()   # pylint: disable=protected-access

    def add(self, component, x, y, orient=None) -> None:
        """
        Add a component to the schematic at the given XY location.
        If an orientation is specified, set that as well.
        """

        self.append(component)

        component.location = XY(x, y)
        if orient is not None:
            component.set('orient', str(orient))

        component._ensure_id()              # pylint: disable=protected-access


    def create(self, defn: str, **kwargs) -> UserCmp:
        """
        Create a new User Component from a definition.
        """

        xml = UserCmp.XML.format(defn=defn)
        component = cast(UserCmp, self._parse(xml))

        if kwargs:
            paramlist = cast(ParamListNode, component.find('paramlist'))
            paramlist.create_params(kwargs)

        component._ensure_id()              # pylint: disable=protected-access

        return cast(UserCmp, component)


    @property
    def parameters(self) -> Schematic.Parameters:
        """
        Retrieve the Schematic's Parameters
        """

        return self.Parameters(self.find('paramlist'))


    #-----------------------------------------------------------------------

    class Parameters(ParametersBase):   # pylint: disable=too-few-public-methods
        """
        Schematic parameters
        """

        # All canvases
        show_grid: int
        size: int
        orient: int
        show_border: int

        # Additional user canvas parameters
        show_signal: int
        show_virtual: int
        show_sequence: int
        auto_sequence: int
        monitor_bus_voltage: int
        show_terminals: int
        virtual_filter: str
        animation_freq: int
