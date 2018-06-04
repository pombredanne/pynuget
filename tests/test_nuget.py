# -*- coding: utf-8 -*-
"""
"""
import os
import subprocess

import pytest

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
NUGET_EXE = "/home/dthor/temp/nuget.exe"
SOURCE = "http://localhost:5000"

@pytest.mark.integration
def test_nuget_metadata(client):
    # happens during list
    # GET http://localhost:5000/$metadata
    pass


@pytest.mark.integration
@pytest.mark.temp
def test_nuget_list(populated_db):
    # GET http://localhost:5000/Search()?$orderby=Id&searchTerm=''&targetFramework=''&includePrerelease=true&$skip=0&$top=30&semVerLevel=2.0.0

    cmd = [
        'mono', NUGET_EXE,
        'list',
        '-Source', SOURCE,
        '-Verbosity', 'detailed',
        '-AllVersions',
        '-Prerelease',
    ]

    subprocess.run(cmd)


@pytest.mark.integration
def test_nuget_add(client):
    # PUT http://localhost:5000/api/v2/package/
    pass


@pytest.mark.integration
def test_nuget_delete(populated_db):
    # DELETE http://localhost:5000/api/v2/package/NuGetTest/0.0.1
    pass


@pytest.mark.integration
def test_nuget_install(populated_db):
    # GET http://localhost:5000/Packages(Id='NuGetTest',Version='0.0.2')
    # GET http://localhost:5000/FindPackagesById()?id='NuGetTest'&semVerLevel=2.0.0
    pass


@pytest.mark.integration
def test_nuget_update(populated_db):
    # GET http://localhost:5000/FindPackagesById()?id='MSTest.TestFramework'&semVerLevel=2.0.0
    pass