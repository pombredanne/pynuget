# -*- coding: utf-8 -*-
"""
"""

import datetime as dt
import json

import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
engine = sa.create_engine('sqlite:///:memory:', echo=False)


class Package(Base):
    """
    """

    __tablename__ = "package"

    package_id = Column(Integer, primary_key=True)
    title = Column(String(256), index=True)
    download_count = Column(Integer, index=True, nullable=False, default=0)
    latest_version = Column(Text())

    def __repr__(self):
        return "<Package({}, {})>".format(self.package_it, self.title)


class Version(Base):
    """
    """

    __tablename__ = "version"

    version_id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("package.package_id"))
    title = Column(Text())
    description = Column(Text())
    created = Column(Integer)
    version = Column(String(32), index=True)
    package_hash = Column(Text())
    package_hash_algorithm = Column(Text())
    dependencies = Column(Text())
    pacakge_size = Column(Integer)
    release_notes = Column(Text())
    version_download_count = Column(Integer, nullable=False, default=0)
    tags = Column(Text())
    license_url = Column(Text())
    project_url = Column(Text())
    icon_url = Column(Text())
    authors = Column(Text())
    owners = Column(Text())
    require_license_acceptance = Column(Boolean())
    copyright_ = Column(Text())
    is_prerelease = Column(Boolean())

    package = relationship("Package", backref="versions")

    def __repr__(self):
        return "<Version({}, {})>".format(self.package.title, self.version)


def count_packages(session):
    """Count the number of packages on the server."""
    return session.query(func.count(Package.package_id)).scalar()


def search_packages(session,
                    include_prerelease=False,
                    order_by=desc(Version.version_download_count),
                    filter_=None,
                    search_query=None):

    query = session.query(Version).join(Package)

    if search_query is not None:
        search_query = "%" + search_query + "%"
        query = query.filter(
            or_(Package.title.like(search_query),
                Package.package_id.like(search_query)
                )
        )

    if not include_prerelease:
        query = query.filter(Version.is_prerelease.isnot(True))

    known_filters = ('is_absolute_latest_version', 'is_latest_version')
    if filter_ is None:
        pass
    elif filter_ in known_filters:
        query = query.filter(Version.version == Package.latest_version)
    else:
        raise ValueError("Unknown filter '{}'".format(filter_))

    if order_by is not None:
        query = query.order_by(order_by)

    return query.all()


def package_updates():
    raise NotImplementedError


def find_by_id(session, package_id, version=None):
    """Find a package by ID and version. If no version given, return all."""
    query = session.query(Version).filter(Version.package_id == package_id)
    if version:
        query = query.filter(Version.version == version)
    query.order_by(desc(Version.version))

    return query.all()


def parse_order_by():
    raise NotImplementedError


def do_search():
    raise NotImplementedError


def validate_id_and_version(session, package_id, version):
    """Not exactly sure what this is supposed to do, but I *think* it simply
    makes sure that the given pacakge_id and version exist... So that's
    what I've decided to make it do."""
    query = (session.query(Version)
             .filter(Version.package_id == package_id)
             .filter(Version.version == version)
             )
    return session.query(query.exists()).scalar()


def increment_download_count(session, package_id, version):
    """Increment the download count for a given package version."""
    obj = (session.query(Version)
           .filter(Version.package_id == package_id)
           .filter(Version.version == version)
           ).one()
    obj.version_download_count += 1
    obj.package.download_count += 1
    session.commit()


def insert_or_update_package():
    raise NotImplementedError


def insert_version(session, **kwargs):
    """Insert a new version of an existing package."""
    kwargs['created'] = dt.datetime.utcnow()
    if 'dependencies' in kwargs:
        kwargs['dependencies'] = json.dumps(kwargs['dependencies'])
    if 'is_prerelease' not in kwargs:
        kwargs['is_prerelease'] = 0
    if 'require_license_acceptance' not in kwargs:
        kwargs['require_license_acceptance'] = 0

    version = Version(**kwargs)
    session.add(version)
    session.commit()


def delete_version():
    raise NotImplementedError


# XXX: I don't think this is actually needed, since SQLAlchemy does it.
def build_in_clause():
    raise NotImplementedError
