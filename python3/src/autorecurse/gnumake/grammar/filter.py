from autorecurse.lib.line import Line
from autorecurse.lib.stream import Condition
import re


class FileSectionFilter(Condition[Line]):
    """
    Outputs the lines between _START_LINE and _END_LINE, when used with
    a ConditionFilter. _START_LINE and _END_LINE denote the target
    definition section in the output of `make -np`

    ## Transition System Definition

    ### States

    - N = No printing <- INITIAL
    - Y = Printing
    - B = Before printing
    - F = Finished

    ### Transition Labels

    - Start = Recieve Line equal to _START_LINE
    - End = Recieve Line equal to _END_LINE
    - Line = Recieve Line not equal to _START_LINE or _END_LINE

    ### Transitions Grouped by Label

    - Start
      - N -> B
      - Y -> Y
      - B -> Y
      - F -> F
    - End
      - N -> N
      - Y -> F
      - B -> N
      - F -> F
    - Line
      - N -> N
      - Y -> Y
      - B -> Y
      - F -> F
    """

    _START_LINE = Line.make('# Files')
    _END_LINE = Line.make('# files hash-table stats:')

    # States
    _NO_PRINTING = 0
    _PRINTING = 1
    _BEFORE_PRINTING = 2
    _FINISHED = 3

    # Transition Labels
    _START = 0
    _END = 1
    _LINE = 2

    # Keys are tuples of (state, transition_label)
    _TRANSITIONS = {
            (_NO_PRINTING, _START): _BEFORE_PRINTING,
            (_PRINTING, _START): _PRINTING,
            (_BEFORE_PRINTING, _START): _PRINTING,
            (_FINISHED, _START): _FINISHED,
            (_NO_PRINTING, _END): _NO_PRINTING,
            (_PRINTING, _END): _FINISHED,
            (_BEFORE_PRINTING, _END): _NO_PRINTING,
            (_FINISHED, _END): _FINISHED,
            (_NO_PRINTING, _LINE): _NO_PRINTING,
            (_PRINTING, _LINE): _PRINTING,
            (_BEFORE_PRINTING, _LINE): _PRINTING,
            (_FINISHED, _LINE): _FINISHED
            }

    def __init__(self) -> None:
        super().__init__()
        self._state = None # type: int

    @staticmethod
    def make() -> 'FileSectionFilter':
        instance = FileSectionFilter()
        FileSectionFilter._setup(instance)
        return instance

    @staticmethod
    def _setup(instance: 'FileSectionFilter') -> None:
        instance._state = FileSectionFilter._NO_PRINTING

    def _set_current_item(self, value: Line) -> None:
        if value.content == FileSectionFilter._START_LINE.content:
            self._do_transition(FileSectionFilter._START)
        elif value.content == FileSectionFilter._END_LINE.content:
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


class DatabaseSectionFilter(Condition[Line]):
    """

    Outputs the lines after _START_LINE (including _START_LINE) when
    used with a ConditionFilter. _START_LINE denotes the make database
    section in the output of `make -np`. Since `make -np` outputs
    recipes before outputting the make database, _START_LINE was chosen
    to minimize the chance of collision with possible recipe lines.

    ## Transition System Definition

    ### States

    - N = No printing <- INITIAL
    - Y = Printing

    ### Transition Labels

    - Start = Recieve Line equal to _START_LINE
    - Line = Recieve Line not equal to _START_LINE

    ### Transitions Grouped by Label

    - Start
      - N -> Y
      - Y -> Y
    - Line
      - N -> N
      - Y -> Y
    """

    _START_LINE = Line.make('# Pattern-specific Variable Values')

    # States
    _NO_PRINTING = 0
    _PRINTING = 1

    # Transition Labels
    _START = 0
    _LINE = 1

    # Keys are tuples of (state, transition_label)
    _TRANSITIONS = {
            (_NO_PRINTING, _START): _PRINTING,
            (_PRINTING, _START): _PRINTING,
            (_NO_PRINTING, _LINE): _NO_PRINTING,
            (_PRINTING, _LINE): _PRINTING,
            }

    def __init__(self) -> None:
        super().__init__()
        self._state = None # type: int

    @staticmethod
    def make() -> Condition[Line]:
        instance = DatabaseSectionFilter()
        instance._state = DatabaseSectionFilter._NO_PRINTING
        return instance

    def _set_current_item(self, value: Line) -> None:
        if value.content == DatabaseSectionFilter._START_LINE.content:
            self._do_transition(DatabaseSectionFilter._START)
        else:
            self._do_transition(DatabaseSectionFilter._LINE)

    current_item = property(None, _set_current_item)

    @property
    def condition(self) -> bool:
        return self._state == DatabaseSectionFilter._PRINTING

    def _do_transition(self, transition_label: int) -> None:
        self._state = DatabaseSectionFilter._TRANSITIONS[(self._state, transition_label)]

del DatabaseSectionFilter._set_current_item


class InformationalCommentFilter(Condition[Line]):
    """
    Skips informational comments output by `make -np`, when used with a
    ConditionFilter.

    ## Transition System Definition

    ### States

    - Y = Printing <- INITIAL
    - N = No printing

    ### Transition Labels

    - Informational = Recieve Line matching _INFORMATIONAL_RE
    - Line = Recieve Line not matching _INFORMATIONAL_RE

    ### Transitions Grouped by Label

    - Informational
      - Y -> N
      - N -> N
    - Line
      - Y -> Y
      - N -> Y
    """

    _INFORMATIONAL_RE = re.compile(r'^#  ')

    def __init__(self) -> None:
        super().__init__()
        self._printing = None # type: bool

    @staticmethod
    def make() -> 'InformationalCommentFilter':
        instance = InformationalCommentFilter()
        InformationalCommentFilter._setup(instance)
        return instance

    @staticmethod
    def _setup(instance: 'InformationalCommentFilter') -> None:
        instance._printing = True

    def _set_current_item(self, value: Line) -> None:
        if InformationalCommentFilter._INFORMATIONAL_RE.match(value.content) is not None:
            self._printing = False
        else:
            self._printing = True

    current_item = property(None, _set_current_item)

    @property
    def condition(self) -> bool:
        return self._printing

del InformationalCommentFilter._set_current_item


