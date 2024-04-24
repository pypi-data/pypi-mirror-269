from __future__ import annotations
from typing import List, Type
from uuid import UUID
from org.iplatform.common.entities.entity.Entity import Entity
class Asset(Entity['Asset']):
    def __init__(self, id: UUID = None, name: str = "", description: str = "", parent: object = None) -> None:
        self.id = id
        self.parent = parent
        self.name = name
        self.description = description
    def addEntity(self, entity: Asset) -> bool:
        return super().addEntity(entity)
    def removeEntity(self, entity: Asset) -> bool:
        return super().removeEntity(entity)
    def modifyEntity(self, entity: Asset) -> bool:
        return super().modifyEntity(entity)
    def findEntityByName(self, name: str) -> List[Asset]:
        return super().findEntityByName(name)
    def findEntityByID(self, name: str) -> List[Asset]:
        return super().findEntityByID(name)
    
    def addAsset(self, asset: Type['Asset']) -> bool:
        result = self.addEntity(asset)
        return result
    def removeAsset(self, asset: Type['Asset']) -> bool:
        result = self.removeEntity(asset)
        return result
    def modifyAsset(self, asset: Type['Asset']) -> bool:
        result = self.modifyEntity(asset)
        return result
    def findAssetByName(self, name: str) -> List['Asset']:
        result = self.findAssetByName(name)
        return result
    def findAssetById(self, id: UUID) -> List['Asset']:
        result = self.findAssetById(id)
        return result
