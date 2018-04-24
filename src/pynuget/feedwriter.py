# -*- coding: utf-8 -*-
"""
"""

import datetime as dt
import json
import re

class FeedWriter(object):

    def __init__(self, id_):
        self.feed_id = id_
        self.base_url = 'TBD'

    def write(self):
        self.begin_feed()
        for result in results:
            self.add_entry(result)
        return self.feed.as_xml()

    def write_to_output(self, results):
        raise NotImplementedError

    def begin_feed(self):
        raise NotImplementedError

    def add_entry(self):
        raise NotImplementedError

    def add_entry_meta(self):
        raise NotImplementedError

    def render_meta_date(self, date)
        return {'value': cls.format_date(date), 'type': dt.datetime}

    def render_meta_boolean(self, value):
        return {'value': value, type: bool}

    def format_date(self):
        #  return dt.isoformat(timespec='seconds')      # Py3.6+
        return dt.isoformat()

    def render_dependencies(self, raw):
        if not raw:
            return ''

        data = json.loads(raw)
        if not data:
            return ''

        output = []

        for dependency in data:
            formatted_dependency = dependency.id + dependency.version
            if dependency.framework:
                formatted_dependency += self.format_target_framework(dependency.framework)
            output.append(formatted_dependency)

        return "|".join(output)


    def format_target_framework(self, framework):
        """Format a raw target framework from a NuSpec into the format
        used in the packages feed.

        Eg:
        DNX4.5.1 -> dnx451
        DNXCore5.0 -> dnxcore50
        """
        return re.sub('[^A-Z0-9]', '', framework).lower()

    def add_with_attributes(self, entry, name, value, attributes):
        """

        Parameters
        ----------
        entry :
            Looks to be a SimpleXMLElement node object
        attributes :
            Dict, I think.
        """
        node = entry.add_child(name, value)
        for attr_name, attr_value in attributes.items():
            node.add_attributes(attr_name, attr_value)

    def add_meta(self, entry, name, value, type_=None):
        ado_url = 'http://schemas.microsoft.com/ado/2007/08/dataservices',
        node = entry.add_child(
            name,
            value,
            ado_url,
        )

        if type_:
            node.add_attribute(
                'm:type',
                type_,
                ado_url,
            )

        if value is None:
            node.add_attribute(
                'm:null',
                'true',
                ado_url,
            )
