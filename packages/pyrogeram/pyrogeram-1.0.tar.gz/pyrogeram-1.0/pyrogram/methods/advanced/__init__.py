#  FORK PYROFORK <http://www.gnu.org/licenses/>.

from .invoke import Invoke
from .resolve_peer import ResolvePeer
from .save_file import SaveFile


class Advanced(
    Invoke,
    ResolvePeer,
    SaveFile
):
    pass
