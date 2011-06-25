from journalists.models import Journalist
from reversion.models import Version

FIELD_INDEXES = {
  Journalist: {'indexed': ['description']},
  Version: {'indexed': ['object_id']},
}
