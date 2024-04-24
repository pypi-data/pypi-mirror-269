import time
from datetime import timedelta
import boto3
import pyotp


class Okta:
    def __init__(self, **kwargs):
        self.__okta_username = kwargs.get("username")
        self.__okta_totp = kwargs.get("totp")
        self.__client_name = kwargs.get("client_name")
        self.__role_name = kwargs.get("role_name")
        self.__account_id = kwargs.get("account_id")
        self.__client_type = kwargs.get("client_type")
        self.__service_name = kwargs.get("service_name")
        self.__region_name = kwargs.get("region_name")
        self.__start_url = kwargs.get("start_url")

    def get_aws_session(self):
        session = boto3.Session()
        sso_client = session.client(
            self.__service_name,
            region_name=self.__region_name,
        )

        register_response = sso_client.register_client(clientName=self.__client_name, clientType=self.__client_type)

        sso_device_auth_response = sso_client.start_device_authorization(
            clientId=register_response["clientId"],
            clientSecret=register_response["clientSecret"],
            startUrl=self.__start_url,
        )

        self.__okta_auth(sso_device_auth_response["verificationUriComplete"])
        token_response = sso_client.create_token(
            grantType="urn:ietf:params:oauth:grant-type:device_code",
            clientId=register_response["clientId"],
            clientSecret=register_response["clientSecret"],
            deviceCode=sso_device_auth_response["deviceCode"],
        )

        sso = session.client("sso", region_name=self.__region_name)
        account_roles = sso.list_account_roles(accessToken=token_response["accessToken"], accountId=self.__account_id)
        roles = account_roles["roleList"]
        result = [role for role in roles if role["roleName"].__contains__(self.__role_name)]
        if len(result) == 0:
            role = roles[0]
        else:
            role = result[0]
        role_creds = sso.get_role_credentials(
            roleName=role["roleName"],
            accountId=role["accountId"],
            accessToken=token_response["accessToken"],
        )

        session = boto3.Session(
            region_name=self.__region_name,
            aws_access_key_id=role_creds["roleCredentials"]["accessKeyId"],
            aws_secret_access_key=role_creds["roleCredentials"]["secretAccessKey"],
            aws_session_token=role_creds["roleCredentials"]["sessionToken"],
        )
        return session

    def __okta_auth(self, verification_url):
        try:
            from RPA.Browser.Selenium import Selenium
        except ImportError:
            raise ImportError("Rpaframework is not installed. Please install it via pip")

        selenium_wait_time = 30
        browser = Selenium()
        browser.open_available_browser(url=verification_url, headless=True)
        try:
            browser.wait_until_element_is_visible(
                '//button[text() ="Confirm and continue"]', timedelta(seconds=selenium_wait_time)
            )
            browser.click_element('xpath://button[text() ="Confirm and continue"]')
            username_id = "id:okta-signin-username"
            browser.wait_until_element_is_enabled(username_id, timedelta(seconds=selenium_wait_time + 15))
            current_username = browser.get_text(username_id)
            username = str(self.__okta_username).split("@")[0]
            if current_username != username:
                browser.input_text(username_id, username)

            if not browser.is_checkbox_selected('//input[@name="remember"]'):
                browser.click_element_when_visible('xpath://div[@class="custom-checkbox"]')

            browser.click_button("id:okta-signin-submit")
            answer_input = "name:answer"
            browser.wait_until_element_is_enabled(answer_input, timedelta(seconds=selenium_wait_time))

            totp = pyotp.TOTP(self.__okta_totp)
            otp_code = totp.now()
            browser.input_text(answer_input, otp_code)
            browser.click_element('xpath://input[@class="button button-primary"]')

            time.sleep(5)
            button_allow = '//button/*[text()="Allow"]'
            if browser.is_element_visible('//*[text()="Allow access to your data?"]'):
                browser.wait_until_element_is_visible(button_allow)
                browser.click_element(button_allow)

            time.sleep(5)
            login_button = "id:cli_login_button"
            if browser.is_element_visible(login_button):
                browser.wait_until_element_is_enabled(login_button, timedelta(seconds=selenium_wait_time))
                browser.click_element_when_visible(login_button)

            time.sleep(5)
            if browser.is_element_visible("xpath://b[.='Request approved']"):
                browser.wait_until_element_is_visible("xpath://b[.='Request approved']")
        finally:
            browser.close_browser()
