from enum import Enum
from selenium import webdriver, common
from pytimedinput import timedInput


class Status(Enum):
    NONE = "0"
    STOP = "1"


class UserStatus(Enum):
    ADD_PRODUCT = "1"
    AUTO_REFRESH = "2"
    EXIT = "9"


class Shop:
    def __init__(self) -> None:
        super().__init__()
        options = webdriver.ChromeOptions()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("detach", True)
        options.add_experimental_option(
            "prefs",
            {
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False,
            },
        )
        options.add_argument("--disable-software-rasterizer")
        self.web = webdriver.Chrome(options=options)

    def add_product(self) -> None:
        try:
            url = input("請輸入Undergarden商品網址: ")
            print("載入網頁中")
            self.web.get(url)
            while True:  # Search target until find it or interrupt by user.
                try:
                    print("找尋[加入購物車]按鈕")
                    cart = self.web.find_element_by_id(
                        "btn-main-checkout"
                    )  # Find 加入購物車
                    cart.click()  # Click 加入購物車
                    print("加入商品成功")
                    break
                except common.exceptions.ElementNotInteractableException:
                    userText, timedOut = timedInput(
                        "找不到[加入購物車]按鈕，5秒後網頁自動重新整理並嘗試找尋按鈕(輸入0以停止重新整理): "
                    )
                    if userText == "0":
                        print("使用者中斷搜尋")
                        break
                    self.web.refresh()
                except:
                    print("未處理的錯誤，返回功能頁")
                    break
        except:
            print("解析網址發生錯誤，返回功能頁")


if __name__ == "__main__":
    print(
        """
    [使用說明]
    使用此程式前，請先準備Undergarden各項商品的網址，加入商品時，請直接貼上網址，例如下列2個範例
    https://www.undergarden.co/products/goopimade%C2%AE-22aw-%E2%80%9Carchetype-01%E2%80%9D-3d-ls-pocket-tee-bathyal
    https://www.undergarden.co/products/liberaiders-22aw-og-logo-tee
    [注意事項]
    1. 此程式不會記憶任何資訊，如同Google Chrome訪客模式。
    2. 如果使用Ctrl + C中斷程式，則瀏覽器會強制關閉
    """
    )

    status = Status.NONE
    shop = Shop()
    while status != Status.STOP:
        try:
            user_st = input(
                """
    (選項)[功能]
    ({add_product})[加入商品]
    ({exit})[離開程式且網頁不會關閉]
    輸入:""".format(
                    add_product=UserStatus.ADD_PRODUCT.value, exit=UserStatus.EXIT.value
                )
            )

            if user_st == UserStatus.ADD_PRODUCT.value:
                shop.add_product()
            elif user_st == UserStatus.EXIT.value:
                break
            else:
                print("無效的輸入")

        except KeyboardInterrupt:
            print("程式強制結束")
            break
    input("程式結束，小黑窗與瀏覽器不會關閉")
