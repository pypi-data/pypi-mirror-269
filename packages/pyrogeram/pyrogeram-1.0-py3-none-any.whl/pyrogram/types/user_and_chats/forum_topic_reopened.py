#  FORK PYROFORK <http://www.gnu.org/licenses/>.

from ..object import Object


class ForumTopicReopened(Object):
    """A service message about a forum topic reopened in the chat.

    Currently holds no information.
    """

    def __init__(self):
        super().__init__()
