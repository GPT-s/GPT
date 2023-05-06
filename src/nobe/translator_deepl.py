from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time

class DeeplTranslator:

    def __init__(self, headless=True):
        print("딥엘 1번")
        self.headless = headless
        self.driver = self.set_chrome_driver()
        print("딥엘 1번 완")


    def set_chrome_driver(self):
        print("딥엘 2번 시작")
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("headless")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        )
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        print("딥엘 2번 완")
        return driver

    def translate(self, text):
        print("딥엘 3번 시작")
        deepL = None
        try:
            deepL = self.set_chrome_driver()
            deepL.switch_to.window(deepL.window_handles[-1])
            deepL.get("https://www.deepl.com/ko/translator")
            time.sleep(2)
            deepL.find_element(
                By.CSS_SELECTOR,
                ".lmt__textarea.lmt__source_textarea.lmt__textarea_base_style",
            ).send_keys(text)
            time.sleep(2)
            deepL_translated = deepL.find_element(
                By.CSS_SELECTOR, ".lmt__target_textarea"
            )
            time.sleep(4)
            result = deepL_translated.get_attribute("value")
            
            # 번역 결과와 원문 텍스트가 중복되는 경우를 확인
            if text in result:
                # 중복되는 원문 텍스트를 삭제
                result = result.replace(text, "").strip()

        except NoSuchElementException:
            result = "번역 오류ㅠㅠ"
        except Exception as e:
            result = f"번역 오류: {e}"
        finally:
            if deepL is not None:
                try:
                    deepL.close()
                except Exception as e:
                    print(f"브라우저 종료 오류: {e}")
        print("딥엘 3번 완")
        return result