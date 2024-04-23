class ElementAnchorPoint(object):
    """Resource element anchor point"""

    def __init__(self, locator, key):
        self.locator = locator
        self.key = key


class ElementPropertyExtractor(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def extract(self, element):
        pass


class ElementTextExtractor(ElementPropertyExtractor):
    def extract(self, element):
        return element.text


class ElementAttrExtractor(ElementPropertyExtractor):
    def __init__(self, attr_key=None, **kwargs):
        super(ElementAttrExtractor, self).__init__(**kwargs)
        self.attr_key = attr_key

    def extract(self, element):
        if not self.attr_key:
            return None
        return element.get_attribute(self.attr_key)


class ElementTagExtractor(ElementPropertyExtractor):
    def extract(self, element):
        return element.tag_name


extractors = {
    'TEXT': ElementTextExtractor,
    'ATTR': ElementAttrExtractor,
    'TAG': ElementTagExtractor
}


class PropertyOption(object):
    """Defined how to get property value from element"""

    def __init__(self, extractor, anchor_point=None):
        """
        :param extractor: Used to extract value from element. extractor.extract()
        :param anchor_point: If element which used to extract property is different from current searched element,
                             then get element from web page by anchor_point
        """
        self.extractor = extractor
        self.anchor_point = anchor_point
