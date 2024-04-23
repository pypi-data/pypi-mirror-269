import time

from spidersearch.common import log

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = log.logger


def default_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options


class ResourceSpider(object):
    def __init__(self, url, target_ele_anchor_point, next_btn_anchor_point=None,
                 resource_handler=None,
                 pre_btn_anchor_point=None, target_ele_start_index=0):
        """
        :param url: The address of the page to be searched
        :param target_ele_anchor_point: The target element anchor point.
        :param next_btn_anchor_point: The anchor point button for next web page.
        :param pre_btn_anchor_point: The anchor point button for previous web page.
        :param resource_handler: The handler for searched target element
        :param target_ele_start_index: Target resource index, self increasing if target is found.
                                       Used for generating resource name
        """
        self.url = url
        self.target_ele_anchor_point = target_ele_anchor_point
        self.next_btn_anchor_point = next_btn_anchor_point
        self.pre_btn_anchor_point = pre_btn_anchor_point
        self.resource_handler = resource_handler
        self.target_ele_index = target_ele_start_index  # Target resource index, self increasing if target is found

        if self.next_btn_anchor_point and self.pre_btn_anchor_point:
            raise Exception('unsupported both next and pre btn')

    def search(self):
        """Based on the tag element and return
        :returns List<WebElement>
        """
        driver = webdriver.Chrome(options=default_options())
        driver.get(self.url)
        self.execute_once(driver)
        driver.close()

    def execute_once(self, driver):
        # Find target element labels
        elements = driver.find_elements(self.target_ele_anchor_point.locator, self.target_ele_anchor_point.key)
        self.target_ele_index += 1
        if self.resource_handler is not None:
            self.resource_handler.handle(driver, elements,
                                         resource_index=self.target_ele_index,
                                         anchor_point=self.target_ele_anchor_point)

        # For next page and previous page
        for anchor_point in (self.next_btn_anchor_point, self.pre_btn_anchor_point):
            try:
                element_btn = self._search_element(driver, anchor_point)
            except NoSuchElementException as e:
                logger.error('element not found. anchor_point=%s', anchor_point.__dict__, e)
                continue

            if element_btn is not None:
                element_btn.click()
                time.sleep(3)
                self.execute_once(driver)

    def _search_element(self, driver, anchor_point):
        if anchor_point is None:
            return None

        return driver.find_element(anchor_point.locator, anchor_point.key)
