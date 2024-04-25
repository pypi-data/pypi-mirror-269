#  FORK PYROFORK <http://www.gnu.org/licenses/>.

from ..object import Object


class GeneralTopicHidden(Object):
    """A service message about a general topic hidden in the chat.

    Currently holds no information.
    """

    def __init__(self):
        super().__init__()
