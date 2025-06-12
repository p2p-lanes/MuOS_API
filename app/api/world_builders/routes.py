from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.world_builders import schemas
from app.api.world_builders.crud import world_builder as world_builder_crud
from app.core.database import get_db
from app.core.security import TokenData, get_current_user

router = APIRouter()


@router.get('/', response_model=list[schemas.WorldBuilder])
def get_world_builders(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return world_builder_crud.find(
        db=db,
        user=current_user,
        filters=schemas.WorldBuilderFilter(email=current_user.email),
    )


@router.post('/', response_model=schemas.WorldBuilder)
def create_world_builder(
    world_builder: schemas.WorldBuilderCreate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return world_builder_crud.create(db=db, obj_in=world_builder, user=current_user)
