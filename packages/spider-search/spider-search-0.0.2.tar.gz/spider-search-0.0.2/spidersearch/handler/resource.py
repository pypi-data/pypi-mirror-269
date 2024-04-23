import hashlib
import os
import urllib

from spidersearch.common import log

import requests

logger = log.logger


class Resource(object):
    def __init__(self):
        self.name = None
        self.source = None
        self.index = None
        self.sub_index = None
        self.slibing_count = 0
        self.attrs = {}

    def set_attr(self, key, value):
        self.attrs[key] = value

    def get_attr(self, key):
        return self.attrs.get(key, None)


class DownloadOption(object):
    def __init__(self, download_now=False, name_property_option=None, page_as_snapshot=False, element_as_snapshot=False,
                 source_property_option=None, directory=None, with_name_prefix=True):
        """
        Effective order: download_now > page_as_snapshot > element_as_snapshot > source(+name)
        :param download_now: Download now or not
        :param name_property_option: Define the file name option
        :param page_as_snapshot: Save web page as snapshot and download.
                            if the name_property_option not provided, then use hash(page_url) as file name
        :param element_as_snapshot: Save current element as snapshot and download.
                            if the name_property_option not provided, the use hash(element_id) as file name
        :param source_property_option: Define the file source option
                            if the name_property_option not provided, the use last part text split by '/' as file name
        :param with_name_prefix: auto append name prefix with resource order
        """
        self.download_now = download_now
        self.page_as_snapshot = page_as_snapshot
        self.element_as_snapshot = element_as_snapshot
        self.source_property_option = source_property_option
        self.name_property_option = name_property_option
        self.directory = directory if directory else './'
        self.with_name_prefix = with_name_prefix


class ResourceHandler(object):
    """Handle searched resource"""

    def __init__(self, download_option=None, **kwargs):
        self.download_option = download_option
        self.kwargs = kwargs

    def handle(self, driver, elements, resource_index=None, anchor_point=None, **kwargs):
        if not driver or not elements:
            return

        for idx, element in enumerate(elements):
            resource = self._gen_model(driver, element, idx, elements,
                                       resource_index=resource_index, anchor_point=anchor_point, **kwargs)
            logger.info('generated resource %s', resource.__dict__)
            self._download(resource, driver, element)

    def _gen_model(self, driver, element, sub_index, elements, resource_index=None, anchor_point=None, **kwargs):
        resource = Resource()
        resource.name = driver.title
        resource.source = driver.current_url
        resource.sub_index = sub_index
        resource.index = resource_index
        resource.slibing_count = len(elements)
        return resource

    def _download(self, resource, driver, element):
        if not self.download_option or not self.download_option.download_now:
            return

        if self.download_option.name_property_option:
            name = self._get_property_value(self.download_option.name_property_option, driver, element)
        else:
            name = resource.name

        if self.download_option.page_as_snapshot:
            fn = self._get_target_path(resource, hashlib.sha256(name.encode('utf-8')).hexdigest(), '.png')
            logger.info('save page %s as snapshot. %s', resource.source, fn)
            driver.save_screenshot(fn)
            return

        if self.download_option.element_as_snapshot:
            fn = self._get_target_path(resource, hashlib.sha256(name.encode('utf-8')).hexdigest(), '.png')
            logger.info('save element %s as snapshot. %s', element.id, fn)
            element.screenshot(fn)
            return

        if self.download_option.source_property_option:
            src = self._get_property_value(self.download_option.source_property_option, driver, element)
            if not src:
                logger.info('not found source for element %s', element.id)
                return
            tmp = src.split('.')
            name_from_src = src.split('/')[-1]
            ff = '.' + tmp[-1] if len(tmp) > 1 else ''
            filename = name + ff if name else name_from_src
            fn = self._get_target_path(resource, filename, ff)
            logger.info('download element %s source %s as %s', element.id, urllib.request.unquote(src), fn)
            download(urllib.request.unquote(src), fn)
            return

    def _get_property_value(self, property_option, driver, element):
        if not property_option:
            return None

        ap = property_option.anchor_point
        e = element if not ap else driver.find_element(ap.locator, ap.key)
        return property_option.extractor.extract(e)

    def _get_target_path(self, resource, filename, extension):
        directory = self.download_option.directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        fn = filename + ('' if filename.endswith(extension) else extension)
        if self.download_option.with_name_prefix:
            fn = '{}{}-{}'.format(str(resource.index).zfill(5),
                                  '' if resource.slibing_count <= 1 else '-' + str(resource.sub_index).zfill(4),
                                  fn)
        return os.path.join(self.download_option.directory, fn)


def download(uri, path):
    resp = requests.get(uri)
    if resp.status_code >= 300:
        logger.error('download "%s" failed. status_code=%s, reason=%s, headers=%s', uri,
                     resp.status_code, resp.reason, resp.headers)
        return
    with open(path, 'wb') as f:
        f.write(resp.content)
