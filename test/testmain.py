from selenium.webdriver.common.by import By

from core.models import SiteSettings


# page_url = localhost:8000
class IntegrationTest(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://localhost:8000"

    def test_page_title(self):
        """Test if the page title is correct"""
        self.driver.get(self.url)
        expected_title = SiteSettings.title
        actual_title = self.driver.title
        assert (
            actual_title == expected_title
        ), f"Expected title '{expected_title}', but got '{actual_title}'"

    def test_meta_description(self):
        """Test if the meta description is correct"""
        self.driver.get(self.url)
        expected_description = SiteSettings.description
        meta_description = self.driver.find_element(
            By.CSS_SELECTOR, 'meta[name="description"]'
        ).get_attribute("content")
        assert (
            meta_description == expected_description
        ), f"Expected description '{expected_description}', but got '{meta_description}'"

    def test_meta_keywords(self):
        """Test if the meta keywords are correct"""
        self.driver.get(self.url)
        expected_keywords = SiteSettings.keywords
        meta_keywords = self.driver.find_element(
            By.CSS_SELECTOR, 'meta[name="keywords"]'
        ).get_attribute("content")
        assert (
            meta_keywords == expected_keywords
        ), f"Expected keywords '{expected_keywords}', but got '{meta_keywords}'"

    def run_all_tests(self):
        """Run all tests and return results"""
        test_results = {"title": False, "description": False, "keywords": False}

        try:
            self.test_page_title()
            test_results["title"] = True
        except AssertionError as e:
            print(f"Title test failed: {str(e)}")

        try:
            self.test_meta_description()
            test_results["description"] = True
        except AssertionError as e:
            print(f"Description test failed: {str(e)}")

        try:
            self.test_meta_keywords()
            test_results["keywords"] = True
        except AssertionError as e:
            print(f"Keywords test failed: {str(e)}")

        return test_results
