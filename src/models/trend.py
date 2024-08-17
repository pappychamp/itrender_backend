import uuid
from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.setting import Base


# Siteモデル
class Site(Base):
    __tablename__ = "sites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)

    trend_data = relationship("TrendData", back_populates="site")

    def __repr__(self):
        return f"<Site(name={self.name})>"


# 中間テーブル
tag_trend_data = Table(
    "tagtrenddata",
    Base.metadata,
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
    Column("trend_id", UUID(as_uuid=True), ForeignKey("trenddata.id"), primary_key=True),
)


# Tagモデル
class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Tag(name={self.name})>"


# TrendDataモデル
class TrendData(Base):
    __tablename__ = "trenddata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    title = Column(String(255), nullable=False)
    ranking = Column(Integer, nullable=True)
    category = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=False)
    url = Column(String(255), nullable=True)
    embed_html = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Tokyo")), nullable=False)

    site = relationship("Site", back_populates="trend_data")
    tags = relationship(
        "Tag",
        secondary=tag_trend_data,
    )

    def __repr__(self):
        return f"<TrendData(title={self.title})>"
