from typing import List, Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.base_crud import CRUDBase
from app.api.products import models, schemas
from app.core.security import TokenData


class CRUDProduct(
    CRUDBase[models.Product, schemas.ProductCreate, schemas.ProductUpdate]
):
    def find(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[BaseModel] = None,
        user: Optional[TokenData] = None,
        sort_by: str = 'created_at',
        sort_order: str = 'desc',
    ) -> List[models.Product]:
        query = db.query(self.model)
        query = self._apply_filters(query, filters)

        if user:
            allowed_exists = db.query(
                models.ProductAllowedCitizen.product_id
            ).filter(
                models.ProductAllowedCitizen.product_id == models.Product.id,
            ).correlate(models.Product)

            query = query.filter(
                ~allowed_exists.exists()
                | db.query(models.ProductAllowedCitizen)
                .filter(
                    models.ProductAllowedCitizen.product_id == models.Product.id,
                    models.ProductAllowedCitizen.citizen_id == user.citizen_id,
                )
                .correlate(models.Product)
                .exists()
            )

        if not hasattr(self.model, sort_by):
            raise HTTPException(
                status_code=400, detail=f'Invalid sort field: {sort_by}'
            )
        order_by = getattr(self.model, sort_by)
        if sort_order == 'desc':
            order_by = order_by.desc()

        query = query.order_by(order_by)
        return query.offset(skip).limit(limit).all()


product = CRUDProduct(models.Product)
