from .main import dialog as main_dialog
from .guide import dialog as guide_dialog
from .settings import dialog as settings_dialog
from .export import dialog as export_dialog
from .group_choice import dialog as group_choice_dialog
from .schedule import dialog as schedule_dialog
dialogs = [
    main_dialog,
    guide_dialog,
    schedule_dialog,
    settings_dialog,
    export_dialog,
    group_choice_dialog
]