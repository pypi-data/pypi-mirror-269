"""
XML entities for PSCAD definitions
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations

from ast import literal_eval
from collections.abc import MutableMapping
from typing import cast, Any, Iterator, Optional, Union

from lxml import etree as ET

from mhi.xml.node import (XmlNode, NamedNode, NamedIdNode, KeyMapping,
                          ParamNode, NamedNodeContainerMapping,)
from mhi.xml.pscad._project import project_lookup, ProjectMixin

from mhi.xml.pscad.graphics import Graphics
from mhi.xml.pscad.schematic import Schematic


#===============================================================================
# Exports
#===============================================================================


__all__ = ['Definition', 'DefinitionMapping', 'Definitions',
           'Form', 'Category', 'Parameter', ]


#===============================================================================
# Definition
#===============================================================================

@project_lookup.tag('Definition')
class Definition(NamedIdNode, ProjectMixin):
    """
    Definition node
    """


    @property
    def group(self) -> str:
        """
        A comma separated list of groups this definition belongs to.

        Examples::

            '(null)'
            'Miscellaneous,I/O Devices'
            'Meters,Breakers Faults,Machines,Miscellaneous'
        """

        return self.get('group', '')


    @group.setter
    def group(self, group: str) -> None:

        # Delegate to groups setter:
        self.groups = group.split(',')


    @property
    def groups(self) -> list[str]:
        """
        The list of groups this definition belongs to.

        Examples::

            ['(null)']
            ['Miscellaneous', 'I/O Devices']
            ['Meters', 'Breakers Faults', 'Machines', 'Miscellaneous']
        """

        groups = self.get('group', '').split('.')
        groups = [group.strip() for group in groups]
        groups = [group if group else "(null)" for group in groups]

        return groups


    @groups.setter
    def groups(self, groups: list[str]) -> None:

        groups = [group.strip() for group in groups]
        groups = [group if group else "(null)" for group in groups]
        groups = list(dict.fromkeys(groups))  # Remove dups, preserve order
        if not groups:
            groups = ['(null)']

        self.set('group', ','.join(groups))


    @property
    def description(self) -> str:
        """
        Description of the definition
        """

        description = cast(ParamNode,
                           self.find('paramlist/param[@name="Description"]'))
        assert description is not None
        return description.value


    @description.setter
    def description(self, text: str) -> None:

        description = cast(ParamNode,
                           self.find('paramlist/param[@name="Description"]'))
        assert description is not None
        description.value = text


    @property
    def form(self) -> Form:
        """
        The Parameter Form for the definition
        """

        form = self.find('form')
        return cast(Form, form)


    @property
    def schematic(self) -> Schematic:
        """
        The Schematic of the definition, if it is a module definition
        """

        schematic = self.find('schematic')
        return cast(Schematic, schematic)


    @property
    def script(self) -> ScriptSegmentMapping:
        """
        The script dictionary for the definition

        This contains 'Computations', 'Checks', 'Fortran', 'Branch' sections
        (etc).
        """

        script = self.find('script')
        if script is None:
            script = self.makeelement('script')
            self.append_indented(script)

        return ScriptSegmentMapping(cast(XmlNode, script))

    @property
    def graphics(self) -> Graphics:
        """
        The Graphics of the definition
        """

        graphics = self.find('graphics')
        return cast(Graphics, graphics)


    def delete(self) -> None:
        """
        Remove this definition from its parent project
        """

        self._remove_from_parent()


    def __repr__(self) -> str:

        return f"Definition<{self.name}>"


#===============================================================================
# Definitions
#===============================================================================

class DefinitionMapping(NamedNodeContainerMapping[Definition]):
    """
    The project's :class:`.Definition` dictionary.

    Example::

        for defn_name in project.definition:
            print(defn_name)

        main_defn = project.definition['Main']

        del project.definition['not_needed']
    """

    def __init__(self, definitions: Definitions):

        super().__init__(definitions, 'Definition', 'Definitions')


    def _pre_add(self, key: str, defn: Definition): # pylint: disable=arguments-renamed

        project = cast(Definitions, self._container).project
        if project.id_exists(defn.id):
            defn.set('id', str(project.make_id()))

        schematic = defn.schematic
        if schematic is not None:
            for cmp in schematic.components():
                if project.id_exists(cmp.id):
                    cmp.set('id', str(project.make_id()))


#-------------------------------------------------------------------------------

@project_lookup.tag('definitions')
class Definitions(XmlNode, ProjectMixin):
    """
    A `<definitions/>` container node
    """


#===============================================================================
# Scripts
#===============================================================================

class ScriptSegmentMapping(MutableMapping[str, str]):
    """
    The Script dictionary for the `Definition`

    Examples::

        defn.script['Computations'] = "..."
        defn.script['Checks'] = "..."
    """


    def __init__(self, script_node: XmlNode):

        self._script = script_node


    def _find(self, key: str) -> Optional[XmlNode]:

        xpath = f'segment[@name={key!r}]'
        segment = cast(XmlNode, self._script.find(xpath))
        return segment


    def _get(self, key: str) -> XmlNode:

        segment = self._find(key)
        if segment is None:
            raise KeyError(key)
        return segment


    def __contains__(self, key) -> bool:

        assert isinstance(key, str)

        return self._find(key) is not None


    def __getitem__(self, key: str) -> str:

        segment = self._get(key)
        if segment is not None:
            text = ET.tostring(segment, encoding=str, method='text',
                               with_tail=False)
        else:
            text = ''
        return text


    def __setitem__(self, key: str, script: str) -> None:

        segment = self._find(key)
        if segment is None:
            iid = self._script._file.make_id()
            segment = cast(XmlNode,
                           self._script.makeelement('segment', name=key,
                                                    classid='CoreSegment',
                                                    id=str(iid)))
            self._script.append_indented(segment)
        segment.text = ET.CDATA(script)


    def __delitem__(self, key: str) -> None:

        self._get(key)._remove_from_parent()


    def __iter__(self) -> Iterator[str]:

        yield from cast(list[str], self._script.xpath('segment/@name'))


    def __len__(self) -> int:

        return len(self._script.findall('segment'))


#===============================================================================
# Forms
#===============================================================================

@project_lookup.tag('form')
class Form(NamedNode):
    """
    A collection of categories of parameters, along with their descriptions
    and validity constraints.

    Examples::

        form = definition.form

        # Create a "Extra" category, add 'Author', 'Version' parameters.
        extra = form.category.create("Extra")
        extra.add_text('Author', "Creator")
        extra.add_integer('Version', "Revision number", min=1, default=1)

        # Remove the "Extra" category
        del form.category["Extra"]
    """


    #-----------------------------------------------------------------------

    @property
    def w(self) -> int:
        """
        Width of the dialog form, in pixels.

        Does not include additional width added by dynamic help.
        """

        return int(self.get('w', '320'))

    @w.setter
    def w(self, w: int):
        assert w > 0
        self.set('w', str(w))


    #-----------------------------------------------------------------------

    @property
    def h(self) -> int:
        """
        Height of the dialog form, in pixels
        """

        return int(self.get('h', '400'))


    @h.setter
    def h(self, h: int):
        assert h > 0
        self.set('h', str(h))


    #-----------------------------------------------------------------------

    @property
    def splitter(self) -> int:
        """
        The "Description <--> Value" splitter position, in percent
        """

        return int(self.get('splitter', '50'))


    @splitter.setter
    def splitter(self, splitter: int):
        assert 10 <= splitter <= 90
        self.set('splitter', str(splitter))


    #-----------------------------------------------------------------------

    @property
    def commentlines(self) -> int:
        """
        Number of lines at the bottom of the form for help text.
        """

        return int(self.get('commentlines', '4'))


    @commentlines.setter
    def commentlines(self, commentlines: int):
        assert 0 <= commentlines <= 4
        self.set('commentlines', str(commentlines))


    #-----------------------------------------------------------------------

    @property
    def category(self) -> KeyMapping[Category]:
        """
        Form category dictionary
        """

        return CategoryMapping(self, 'category', 'name', 'Categories')


    #-----------------------------------------------------------------------

    @property
    def parameter(self) -> KeyMapping[Parameter]:
        """
        Form parameter dictionary
        """

        return KeyMapping(self, 'category/parameter', 'name', 'Parameters')


    #-----------------------------------------------------------------------

    def __repr__(self) -> str:

        return f"Form<{self.name}>"


#===============================================================================

@project_lookup.tag('category')
class Category(NamedNode):
    """
    A form category

    Contains 1 or more parameters, and a condition for when the category
    is enabled.
    """


    @property
    def cond(self):
        """
        Category enabled condition expression (read/write)
        """

        cond = self.find('cond')
        return cond.text if cond is not None else 'true'


    @cond.setter
    def cond(self, cond: Union[str, bool]):

        if isinstance(cond, bool):
            cond = "true" if cond else "false"

        cond_node = self.find('cond')
        if cond_node is None:
            cond_node = self.makeelement('cond')
            self.insert(0, cond_node)

        cond_node.text = cond


    #-----------------------------------------------------------------------

    @property
    def parameter(self) -> KeyMapping[Parameter]:
        """
        Category parameter dictionary
        """

        return KeyMapping(self, 'parameter', 'name', 'CategoryParameters')


    #-----------------------------------------------------------------------

    @property
    def create_defaults(self):
        """
        A dictionary of default parameter attribute values, to aide in the
        creation of several similar parameters.

        Example::

            category = form.category.create('Category 1')

            category.create_defaults['group'] = 'Section 1'
            category.create_defaults['unit'] = 'kV'

            category.add_real('A', 'The A parameter', ...)
            category.add_real('B', 'The B parameter', ...)

            # Still in group='Section 1', change 'unit', add 'cond' ...
            category.create_defaults['unit'] = 'kA'
            category.create_defaults['cond'] = 'A<2'

            category.add_real('C', 'The C parameter', ...)
            category.add_real('D', 'The D parameter', ...)
            category.add_real('E', 'The E parameter', unit='ohm')
        """

        if '_create_defaults' not in self.__dict__:
            self._create_defaults = {'group': ''}   # pylint: disable=attribute-defined-outside-init

        return self._create_defaults


    #-----------------------------------------------------------------------

    def create(self, name: str, **kwargs) -> Parameter:
        """
        Create a new parameter.

        If entries have been assigned to `create_defaults`, those will
        be used as defaults for unspecified key=value values
        """


        attrs = {'type', 'description', 'group', 'min', 'max', 'unit',
                 'default', 'empty_allowed', 'animate', 'help_mode', 'help',
                 'cond', 'regex', 'error_msg', 'choices',
                 'content_type', 'intent'}

        if not name.isalnum() or not name[0].isalpha():
            raise ValueError(f"Invalid parameter name: {name!r}")

        type_ = kwargs.get('type', '')
        if type_ not in {'Text', 'Complex', 'Real', 'Integer', 'Choice',
                         'Boolean', 'Table'}:
            raise ValueError(f"Invalid parameter type: {type_!r}")

        kwargs = self.create_defaults | kwargs

        param = self.makeelement('parameter', name=name, type=type_)
        self.append_indented(param)

        for key, value in kwargs.items():
            if key not in attrs:
                raise ValueError(f"Invalid attribute {key!r}")
            if value is not None:
                if isinstance(value, bool):
                    value = 'true' if value else 'false'
                setattr(param, key, str(value))

        return cast(Parameter, param)


    #-----------------------------------------------------------------------

    def add_text(self, name: str, description: str, default: str = '',
                 empty_allowed=True, **kwargs) -> Parameter:
        """
        Create a text parameter.
        """

        return self.create(name, type='Text', description=description,
                           default=default, empty_allowed=empty_allowed,
                           **kwargs)

    def add_integer(self,                   # pylint: disable=too-many-arguments
                    name: str, description: str, default: int = 0,
                    min: Optional[int] = None,  # pylint: disable=redefined-builtin
                    max: Optional[int] = None,  # pylint: disable=redefined-builtin
                    animate: bool = False, **kwargs) -> Parameter:
        """
        Create an Integer parameter.
        """

        return self.create(name, type='Integer', description=description,
                           default=default, min=min, max=max, animate=animate,
                           **kwargs)

    def add_real(self,                      # pylint: disable=too-many-arguments
                 name: str, description: str, default: int = 0,
                 min: Optional[int] = None, # pylint: disable=redefined-builtin
                 max: Optional[int] = None, # pylint: disable=redefined-builtin
                 animate: bool = False, unit: Optional[str] = None,
                 **kwargs) -> Parameter:
        """
        Create a Real parameter.
        """


        return self.create(name, type='Real', description=description,
                           default=default, min=min, max=max, animate=animate,
                           unit=unit, **kwargs)


    #-----------------------------------------------------------------------

    def __repr__(self) -> str:

        return f"Category<{self.name}>"


#===============================================================================

class CategoryMapping(KeyMapping[Category]):
    """
    Form category dictionary
    """

    def create(self, name: str):
        """
        Create a new Category
        """

        container = self._container

        category = cast(Category,
                        container.makeelement('category', name=name))
        container.append_indented(category)
        category.append_indented(container.makeelement('cond'))
        category.cond = True

        return category


#===============================================================================

@project_lookup.tag('parameter')
class Parameter(NamedNode):
    """
    A parameter definition.

    Gives the parameter a symbol name, description, type, units, default value,
    validation attributes (minimum and/or maximum limits, regex),
    and help attributes.
    """


    def _get_node_text(self, tag):

        node = self.find(tag)
        return node.text if node is not None else ''


    def _set_node_text(self, tag, value: Any, cdata: bool = True):

        text = str(value) if value is not None else ''

        node = self.find(tag)
        if node is None:
            node = self.makeelement(tag)
            self.append_indented(node)
        node.text = ET.CDATA(text) if cdata else text


    def _set_attrib(self, key, value: Union[str, int, float, None]):

        if value is not None:
            self.set(key, str(value))
        elif key in self.attrib:    # pylint: disable=unsupported-membership-test
            del self.attrib[key]    # pylint: disable=unsupported-delete-operation


    #-----------------------------------------------------------------------

    @property
    def description(self) -> str:
        """
        Parameter description
        """

        return self.get('desc', '')


    @description.setter
    def description(self, desc: str):

        self.set('desc', desc)


    #-----------------------------------------------------------------------

    @property
    def group(self) -> str:
        """
        Parameter group (set of related parameters in one category)
        """

        return self.get('group', '')


    @group.setter
    def group(self, group: str):

        self.set('group', group)


    #-----------------------------------------------------------------------

    @property
    def type(self) -> str:
        """
        Parameter type (Text, Complex, Real, Integer, Choice, Boolean, Table)
        """

        return self.get('type', 'Text')


    @type.setter
    def type(self, type_: str):

        assert type_ in {'Text', 'Complex', 'Real', 'Integer', 'Choice',
                         'Boolean', 'Table'}
        self.set('type', type_)


    #-----------------------------------------------------------------------

    @property
    def min(self) -> Union[int, float, None]:
        """
        Minimum allowed value (Integer / Real) or length (Text)
        """

        value = self.get('min')
        return literal_eval(value or 'None')


    @min.setter
    def min(self, min_: Union[int, float, None]):

        self._set_attrib('min', min_)


    #-----------------------------------------------------------------------

    @property
    def max(self) -> Union[int, float, None]:
        """
        Maximum allowed value (Integer / Real) or length (Text)
        """

        value = self.get('max')
        return literal_eval(value or 'None')


    @max.setter
    def max(self, max_: Union[int, float, None]):

        self._set_attrib('max', max_)


    #-----------------------------------------------------------------------

    @property
    def unit(self) -> str:
        """
        Parameter unit (kV, kA, ohm, MVA, rad/s, ...)
        """

        return self.get('unit', '')


    @unit.setter
    def unit(self, unit: Optional[str]):

        self._set_attrib('unit', unit)


    #-----------------------------------------------------------------------

    @property
    def empty_allowed(self) -> bool:
        """
        Can this Text field be empty?
        """

        return self.get('allowemptystr', 'true') == 'true'


    @empty_allowed.setter
    def empty_allowed(self, value: Union[bool, str]):

        if isinstance(value, bool):
            value = "true" if value else "false"

        self.set('allowemptystr', value)


    #-----------------------------------------------------------------------

    @property
    def animate(self) -> bool:
        """
        Is this parameter animated?
        """

        return self.get('animate', 'false') == 'true'


    @animate.setter
    def animate(self, value: Union[bool, str]):

        if isinstance(value, bool):
            value = "true" if value else "false"

        self.set('animate', value)


    #-----------------------------------------------------------------------

    @property
    def help_mode(self) -> str:
        """
        Help mode (Append, Overwrite)
        """

        return self.get('helpmode', 'Append')


    @help_mode.setter
    def help_mode(self, value: str):

        self.set('helpmode', value)


    #-----------------------------------------------------------------------

    @property
    def content_type(self) -> str:
        """
        Parameter context type (Variable, Literal, Constant)
        """

        return self.get('content_type', 'Literal')


    @content_type.setter
    def content_type(self, value: str):

        if value not in {'Variable', 'Literal', 'Constant'}:
            raise ValueError("Invalid content_type: {value!r}")

        self.set('content_type', value)


    #-----------------------------------------------------------------------

    @property
    def intent(self) -> str:
        """
        Parameter context type (Variable, Literal, Constant)
        """

        return self.get('intent', 'Output')


    @intent.setter
    def intent(self, value: str):

        if value not in {'Input', 'Output'}:
            raise ValueError("Invalid content_type: {value!r}")

        self.set('intent', value)


     #-----------------------------------------------------------------------

    @property
    def default(self) -> str:
        """
        Default value for the parameter
        """

        return self._get_node_text('value')


    @default.setter
    def default(self, value: Any):

        self._set_node_text('value', value)


    #-----------------------------------------------------------------------

    @property
    def help(self) -> str:
        """
        Brief help message to Append/Overwrite help panel with
        """

        return self._get_node_text('help')


    @help.setter
    def help(self, text: str):

        self._set_node_text('help', text)


    #-----------------------------------------------------------------------

    @property
    def cond(self) -> str:
        """
        Enable condition for this parameter.
        """

        return self._get_node_text('cond')


    @cond.setter
    def cond(self, cond: Union[bool, str]):

        if isinstance(cond, bool):
            cond = "true" if cond else "false"

        self._set_node_text('cond', cond)


    #-----------------------------------------------------------------------

    @property
    def regex(self) -> str:
        """
        A reg-ex validation pattern for `Text` input parameters
        """

        return self._get_node_text('regex')


    @regex.setter
    def regex(self, reg_ex: str):

        self._set_node_text('regex', reg_ex)


    #-----------------------------------------------------------------------

    @property
    def error_msg(self) -> str:
        """
        The message to display if a issue exists with the entered
        parameter value.
        """

        return self._get_node_text('error_msg')


    @error_msg.setter
    def error_msg(self, msg: str):

        self._set_node_text('error_msg', msg)


   #-----------------------------------------------------------------------

    @property
    def choices(self) -> dict[int, str]:
        """
        The options for a `Choice` parameter
        """

        if self.type != 'Choice':
            raise KeyError(f"Parameter {self.name} is not type='Choice'")

        choices = {int(key): val
                   for key, val in (choice.text.split(" = ", 1)
                                    for choice in self.iterfind('choice')
                                    if choice.text)}
        return choices


    @choices.setter
    def choices(self, values: dict[int, str]):

        if self.type != 'Choice':
            raise KeyError(f"Parameter {self.name} is not type='Choice'")

        for old_choice in self.findall('choice'):
            self.remove(old_choice)

        for key, value in values.items():
            choice = self.makeelement('choice')
            choice.text = ET.CDATA(f"{key} = {value}")
            self.append_indented(choice)


    #-----------------------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.type}<{self.name}={self.default!r}>"
