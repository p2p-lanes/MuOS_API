from typing import Optional

import requests
from sqlalchemy.orm import Session

from app.api.base_crud import CRUDBase
from app.api.world_builders import models, schemas
from app.core.config import settings
from app.core.logger import logger
from app.core.security import TokenData


class CRUDWorldBuilder(
    CRUDBase[
        models.WorldBuilder, schemas.WorldBuilderCreate, schemas.WorldBuilderUpdate
    ]
):
    def create(
        self,
        db: Session,
        obj: schemas.WorldBuilderCreate,
        user: Optional[TokenData] = None,
    ) -> models.WorldBuilder:
        obj.builder_score = self.get_score(obj.world_address).score
        return super().create(db, obj, user)

    def get_score(self, address: str) -> schemas.WorldBuilderScore:
        payload = {
            'jsonrpc': '2.0',
            'method': 'eth_getTransactionCount',
            'params': [address, 'latest'],
            'id': 1,
        }

        headers = {'Content-Type': 'application/json'}

        rpc_url = settings.WORLD_CHAIN_URL
        response = requests.post(rpc_url, headers=headers, json=payload)

        if not response.ok:
            raise Exception(f'Error getting transaction count {response.text}')

        tx_count_hex = response.json()['result']
        tx_count = int(tx_count_hex, 16)
        logger.info('Transaction count for %s: %s', address, tx_count)
        return schemas.WorldBuilderScore(score=tx_count)


world_builder = CRUDWorldBuilder(models.WorldBuilder)
