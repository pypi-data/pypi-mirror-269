import ipih

from pih import A
from pih.consts import CONST
from pih.collections.service import ServiceDescription

NAME: str = "PolibaseDatabase"

HOST = A.CT_H.POLIBASE

VERSION: str = "0.18"


SD: ServiceDescription = ServiceDescription(
    name=NAME,
    host=HOST.NAME,
    description="Polibase database service",
    commands=("create_polibase_database_backup",),
    version=VERSION,
    use_standalone=True,
    standalone_name="plb_db",
    run_from_system_account=True,
    python_executable_path=CONST.UNKNOWN,
)

TEST_NAME: str = "test"
STUB_DIRECTORY_NAME: str = "stub"
#
POLIBASE_NAME: str = "Polibase"
ARCHIVE_TYPE: str = A.CT_F_E.ARCHIVE
COMPRESSION_RATIO: int = 9


USE_PRECONNECTED_DISKS: bool = True

class MOUNT_POINT:
    POLIBASE: str = "C"
    NAS: str = "K"
    POLIBASE2: str = "L"


class PRECONNECTED_MOUNT_POINT(MOUNT_POINT):
    NAS: str = "N"
    POLIBASE2: str = "T"


class DATABASE_DUMP:
    FILE_NAME: str = "DatabaseDump"
    RESULT_FILE_NAME: str = "IN"
    FILE_EXTENSION: str = "DMP"
