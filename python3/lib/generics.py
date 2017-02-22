from abc import ABCMeta, abstractmethod
import io
from typing import TypeVar, Generic


T_co = TypeVar('T_co', covariant=True)
class Iterator(Generic[T_co], metaclass=ABCMeta):

    @property
    @abstractmethod
    def current_item(self) -> T_co:
        pass

    @property
    @abstractmethod
    def has_current_item(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_at_start(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_at_end(self) -> bool:
        pass

    @abstractmethod
    def move_to_next(self) -> None:
        pass

    def move_to_end(self) -> None:
        while not self.is_at_end:
            self.move_to_next()

del T_co


T_contra = TypeVar('T_contra', contravariant=True)
class StreamCondition(Generic[T_contra], metaclass=ABCMeta):

    @abstractmethod
    def _set_current_item(self, value: T_contra) -> None:
        pass

    current_item = property(None, _set_current_item)

    @property
    @abstractmethod
    def condition(self) -> bool:
        pass

del StreamCondition._set_current_item
del T_contra


class LineBreakError(Exception):

    def __init__(self, message: str = None) -> None:
        if message is None:
            super().__init__("String has multiple line breaks.")
        else:
            super().__init__(message)


class Line:

    @staticmethod
    def make(content: str) -> 'Line':
        instance = Line()
        Line._setup(instance, content)
        return instance

    @staticmethod
    def _setup(instance: 'Line', content: str) -> None:
        lines = content.splitlines()
        if len(lines) == 1:
            instance._content = lines[0]
        elif len(lines) == 0:
            instance._content = ''
        else:
            raise LineBreakError()

    @property
    def content(self) -> str:
        return self._content

    def __str__(self) -> str:
        return self.content

    def __eq__(self, other: 'Line') -> bool:
        return ((other.__class__ is self.__class__)
            and (self.content == other.content))

    def __hash__(self) -> int:
        return hash(self.content)


class FileLineIterator(Iterator[Line]):

    @staticmethod
    def make(fp: io.TextIOBase) -> 'FileLineIterator':
        instance = FileLineIterator()
        FileLineIterator._setup(instance, fp)
        return instance

    @staticmethod
    def _setup(instance: 'FileLineIterator', fp: io.TextIOBase) -> None:
        instance._file = fp
        instance._line = None
        instance._is_at_end = False

    @property
    def current_item(self) -> Line:
        return self._line

    @property
    def has_current_item(self) -> bool:
        return self._line is not None

    @property
    def is_at_start(self) -> bool:
        return not (self.has_current_item or self.is_at_end)

    @property
    def is_at_end(self) -> bool:
        return self._is_at_end

    def move_to_next(self) -> None:
        line = self._file.readline()
        if len(line) == 0: # End of file
            self._is_at_end = True
            self._line = None
        else:
            self._line = Line.make(line)


class EmptyLineFilter(StreamCondition[Line]):

    _EMPTY_LINE = Line.make('')

    @staticmethod
    def make() -> 'EmptyLineFilter':
        instance = EmptyLineFilter()
        EmptyLineFilter._setup(instance)
        return instance

    @staticmethod
    def _setup(instance: 'EmptyLineFilter') -> None:
        instance._line = None

    def _set_current_item(self, value: Line) -> None:
        self._line = value

    current_item = property(None, _set_current_item)

    @property
    def condition(self) -> bool:
        return self._line != EmptyLineFilter._EMPTY_LINE

del EmptyLineFilter._set_current_item


class FileSectionFilter(StreamCondition[Line]):
    """
    Outputs the lines between _START_LINE and _END_LINE, when used with
    a ConditionalSkipIterator.

    ## Transition System Definition

    ### States

    - N = No printing <- INITIAL
    - Y = Printing
    - B = Before printing

    ### Transition Labels

    - Start = Recieve Line equal to _START_LINE
    - End = Recieve Line equal to _END_LINE
    - Line = Recieve Line not equal to _START_LINE or _END_LINE

    ### Transitions Grouped by Label

    - Start
      - N -> B
      - Y -> Y
      - B -> Y
    - End
      - N -> N
      - Y -> N
      - B -> N
    - Line
      - N -> N
      - Y -> Y
      - B -> Y
    """

    _START_LINE = Line.make('# Files')
    _END_LINE = Line.make('# files hash-table stats:')

    # States
    _NO_PRINTING = 0
    _PRINTING = 1
    _BEFORE_PRINTING = 2

    # Transition Labels
    _START = 0
    _END = 1
    _LINE = 2

    # Keys are tuples of (state, transition_label)
    _TRANSITIONS = {
            (_NO_PRINTING, _START): _BEFORE_PRINTING,
            (_PRINTING, _START): _PRINTING,
            (_BEFORE_PRINTING, _START): _PRINTING,
            (_NO_PRINTING, _END): _NO_PRINTING,
            (_PRINTING, _END): _NO_PRINTING,
            (_BEFORE_PRINTING, _END): _NO_PRINTING,
            (_NO_PRINTING, _LINE): _NO_PRINTING,
            (_PRINTING, _LINE): _PRINTING,
            (_BEFORE_PRINTING, _LINE): _PRINTING
            }

    @staticmethod
    def make() -> 'FileSectionFilter':
        instance = FileSectionFilter()
        FileSectionFilter._setup(instance)
        return instance

    @staticmethod
    def _setup(instance: 'FileSectionFilter') -> None:
        instance._state = FileSectionFilter._NO_PRINTING

    def _set_current_item(self, value: Line) -> None:
        if FileSectionFilter._START_LINE == value:
            self._do_transition(FileSectionFilter._START)
        elif FileSectionFilter._END_LINE == value:
            self._do_transition(FileSectionFilter._END)
        else:
            self._do_transition(FileSectionFilter._LINE)

    current_item = property(None, _set_current_item)

    @property
    def condition(self) -> bool:
        return self._state == FileSectionFilter._PRINTING

    def _do_transition(self, transition_label: int) -> None:
        self._state = FileSectionFilter._TRANSITIONS[(self._state, transition_label)]

del FileSectionFilter._set_current_item

