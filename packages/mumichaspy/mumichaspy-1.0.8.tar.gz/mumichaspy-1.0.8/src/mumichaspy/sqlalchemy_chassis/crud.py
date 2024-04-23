# -*- coding: utf-8 -*-
"""CRUD helpers for SQLAlchemy."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.orm import DeclarativeMeta
from typing import Type, Dict, Any, Optional
import logging


logger = logging.getLogger(__name__)


# Generic CRUD functions ##########################################################################
# READ
async def get_list(
    db: AsyncSession,
    model: Type[DeclarativeMeta],
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    order_by: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
):
    """Retrieve a list of elements from database"""
    stmt = select(model)
    stmt = add_options_to_statement(stmt, offset, limit, order_by, model, filters)
    return await get_list_statement_result(db, stmt)


async def get_element_by_id(
    db: AsyncSession, model: Type[DeclarativeMeta], element_id: Any
):
    """Retrieve any DB element by id."""
    return await db.get(model, element_id)


async def get_list_statement_result(db: AsyncSession, stmt: Select):
    """Execute given statement and return list of items."""
    result = await db.execute(stmt)
    item_list = result.unique().scalars().all()
    return item_list


async def get_first_statement_result(db: AsyncSession, stmt: Select):
    """Execute given statement and return the first item."""
    result = await db.execute(stmt)
    item = result.scalar()
    return item


# DELETE
async def delete_element_by_id(
    db: AsyncSession, model: Type[DeclarativeMeta], element_id: Any
):
    """Delete any DB element by id."""
    element = await get_element_by_id(db, model, element_id)
    if element is not None:
        await db.delete(element)
        await db.commit()
    return element


# CREATE
async def create_element(db: AsyncSession, db_element: Type[DeclarativeMeta]):
    """Insert a element in the database."""

    try:
        db.add(db_element)
        await db.commit()
        await db.refresh(db_element)
    except Exception as exc:
        logger.error(exc)
        await db.rollback()
        db_element = None
    return db_element


# Optional parameters #############################################################################
def set_order_by_to_statement(
    stmt: Select, model: Type[DeclarativeMeta], order_by: Optional[str]
):
    """Adds order by to given statement if needed."""
    if order_by is not None:
        if order_by.startswith("-"):
            stmt = stmt.order_by(getattr(model, order_by[1:]).desc())
        else:
            stmt = stmt.order_by(getattr(model, order_by))
    return stmt


def add_options_to_statement(
    stmt: Select, offset: int, limit: int, order_by: str, model, filters: dict
) -> Select:
    """Adds options to given statement if needed: offset, limit, order_by."""
    stmt = set_order_by_to_statement(stmt, model, order_by)
    if offset is not None:
        stmt = stmt.offset(offset)
    if limit is not None:
        stmt = stmt.limit(limit)
    if filters is not None:
        stmt = set_filters_to_statement(stmt, model, filters)
    return stmt


def set_filters_to_statement(stmt: Select, model, filters: dict) -> Select:
    """Adds filters to given statement if needed."""
    if filters is None:
        return stmt

    for column, value in filters.items():
        if hasattr(model, column):
            stmt = stmt.filter(getattr(model, column) == value)
        else:
            logger.warning(f"Column {column} not found in model {model.__name__}")
    return stmt
