

from sqlalchemy.exc import NoResultFound
from tendril.utils.db import with_db
from .model import ArtefactModel

from tendril.utils import log
logger = log.get_logger(__name__)


@with_db
def get_artefact(id, session=None):
    q = session.query(ArtefactModel).filter_by(id=id)
    return q.one()


def _type_discriminator(type):
    if not type:
        return ArtefactModel
    # if isinstance(type, str):
    #     from tendril.interests import type_codes
    #     return type_codes[type].model
    if issubclass(type, ArtefactModel):
        return type
    logger.warn(f"Did not find a Model Class for Artefact type {type}")
    return ArtefactModel


@with_db
def get_interest_artefacts(interest_id, type=None, label=None, session=None):
    filters = []
    qmodel = _type_discriminator(type)
    if interest_id:
        filters.append(qmodel.interest_id == interest_id)
    if label:
        filters.append(qmodel.label == label)
    q = session.query(qmodel).filter(*filters)
    try:
        return q.all()
    except NoResultFound:
        return None


@with_db
def create_artefact(type, session=None):
    if not type:
        raise ValueError("type cannot be None")
    artefact = ArtefactModel(type=type)
    session.add(artefact)
    return artefact


@with_db
def register_artefact(artefact: ArtefactModel, session=None):
    session.add(artefact)
    return artefact


def preprocess_artefact(artefact):
    if isinstance(artefact, int):
        return artefact
    if isinstance(artefact, ArtefactModel):
        return artefact.id


@with_db
def get_artefact_owner(artefact, session=None):
    artefact_id = preprocess_artefact(artefact)
    artefact = get_artefact(artefact, session=session)
    return artefact.user


@with_db
def creare_artefact_log_entry(artefact_id, action, reference=None, session=None):
    pass


