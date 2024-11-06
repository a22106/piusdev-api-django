from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from testmain import IntegrationTest

def main():
    # Chrome 옵션 설정
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 헤드리스 모드로 실행하려면 주석 해제
    
    # WebDriver 초기화
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # 테스트 실행
        test = IntegrationTest(driver)
        results = test.run_all_tests()
        
        # 결과 출력
        print("\nTest Results:")
        print("-" * 50)
        for test_name, passed in results.items():
            status = "PASSED" if passed else "FAILED"
            print(f"{test_name.capitalize()}: {status}")
        print("-" * 50)
        
    finally:
        # WebDriver 종료
        driver.quit()

if __name__ == "__main__":
    main() 