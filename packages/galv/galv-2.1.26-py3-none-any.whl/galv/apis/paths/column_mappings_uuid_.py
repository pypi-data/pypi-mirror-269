from galv.paths.column_mappings_uuid_.get import ApiForget
from galv.paths.column_mappings_uuid_.delete import ApiFordelete
from galv.paths.column_mappings_uuid_.patch import ApiForpatch


class ColumnMappingsUuid(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
