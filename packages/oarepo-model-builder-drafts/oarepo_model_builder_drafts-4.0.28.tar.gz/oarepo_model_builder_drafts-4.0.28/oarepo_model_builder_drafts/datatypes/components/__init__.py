from .draft import DraftComponent
from .draft_model import (
    DraftDefaultsModelComponent,
    DraftJSONSchemaModelComponent,
    DraftMappingModelComponent,
    DraftParentComponent,
    DraftPIDModelComponent,
    DraftRecordMetadataModelComponent,
    DraftRecordModelComponent,
    DraftResourceModelComponent,
    DraftServiceModelComponent,
    DraftsRecordDumperModelComponent,
    ParentMarshmallowComponent,
    SearchOptionsModelComponent,
)
from .draft_tests import DraftModelTestComponent
from .published_service import PublishedServiceComponent

DRAFT_COMPONENTS = [
    DraftParentComponent,
    DraftComponent,
    DraftRecordModelComponent,
    DraftRecordMetadataModelComponent,
    DraftPIDModelComponent,
    DraftDefaultsModelComponent,
    DraftJSONSchemaModelComponent,
    DraftModelTestComponent,
    DraftMappingModelComponent,
    DraftResourceModelComponent,
    DraftServiceModelComponent,
    PublishedServiceComponent,
    ParentMarshmallowComponent,
    DraftsRecordDumperModelComponent,
    SearchOptionsModelComponent,
]
