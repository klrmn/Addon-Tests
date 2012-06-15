#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
Created on Jun 21, 2010

'''
from unittestzero import Assert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


class Page(object):
    """
    Base class for all Pages.
    """

    def __init__(self, testsetup):
        """
        Constructor
        """
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.api_base_url = testsetup.api_base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout

    def get_url(self, url):
        self.selenium.get(url)

    @property
    def is_the_current_page(self):
        if self._page_title:
            WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)

        Assert.equal(self.selenium.title, self._page_title,
            "Expected page title: %s. Actual page title: %s" % (self._page_title, self.selenium.title))
        return True

    def get_url_current_page(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.current_url

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_element_visible(self, *locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except NoSuchElementException, ElementNotVisibleException:
            return False

    def return_to_previous_page(self):
        self.selenium.back()

    def navigate_hover_menu(self, hover_locator, menu_locator, menu_item_locator):
        """Hover over a menu and click a menu item. 

        Positional arguements:
        hover_locator -- WebDriver compliant tuple
        menu_locator  -- WebDriver compliant tuple
        menu_item_locator -- WebDriver compliant tuple

        Returns nothing

        Throws:
        TimeoutException with message about which locator was not found
        """
        WebDriverWait(self.selenium, 20).until(lambda s: 
            s.find_element(*hover_locator).is_displayed,
            "hover locator not displayed")
        ActionChains(self.selenium).move_to_element(
            self.selenium.find_element(*hover_locator)
        ).perform()
        WebDriverWait(self.selenium, 20).until(lambda s: 
            s.find_element(*menu_locator).is_displayed,
            "menu locator is not displayed")
        ActionChains(self.selenium).move_to_element(
            self.selenium.find_element(*hover_locator)
        ).move_by_offset(
            -20, 0
        ).move_to_element(
            self.selenium.find_element(
                *menu_locator
            )
        ).click(
            self.selenium.find_element(
                *menu_locator
            ).find_element(*menu_item_locator)
        ).perform()

    def hover_menu_options_text(self, hover_locator, menu_locator):
        """Hover over menu and return text of menu options.

        Positional arguements:
        hover_locator -- WebDriver compliant tuple
        menu_locator  -- WebDriver compliant tuple

        Returns:
        string containing text of menu

        Throws:
        TimeoutException with message about which locator was not found

        Other uses:
        Use this method to hover over menu before performing some other check.
        """
        WebDriverWait(self.selenium, 20).until(lambda s: 
            s.find_element(*hover_locator).is_displayed,
            "hover locator not displayed")
        ActionChains(self.selenium).move_to_element(
            self.selenium.find_element(*hover_locator)
        ).perform()
        WebDriverWait(self.selenium, 20).until(lambda s: 
            s.find_element(*menu_locator).is_displayed)
        return self.selenium.find_element(*menu_locator).text
