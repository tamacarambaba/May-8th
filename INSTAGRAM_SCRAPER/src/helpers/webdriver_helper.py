import zipfile
from src.helpers.path_helpers import join_paths
from src.helpers.json_helpers import get_json_value_by_filename_and_key

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#SET Proxy and return webdriver
def get_chrome_driver(base_path:str, use_proxy=False, proxy_host=None, proxy_port=29842, proxy_user="iweber02", proxy_pass="qp9dQbDM", scraping_hidden=False, user_agent=None):
    PROXY_HOST = proxy_host
    PROXY_PORT = proxy_port
    PROXY_USER = proxy_user
    PROXY_PASS = proxy_pass
 
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
 
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
 
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
 
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
 
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    service = Service(executable_path=join_paths(join_paths(base_path, get_json_value_by_filename_and_key(base_path, "dir_paths.json", "drivers")), "chromedriver.exe"))
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  if scraping_hidden else None                       # behaviour not visible on the machine
 
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'
 
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)
    if user_agent:
        options.add_argument('--user-agent=%s' % user_agent)
 
    driver = webdriver.Chrome(service=service, options=options)
    #driver = webdriver.Chrome(options=options)
    return driver


def check_proxy_connection(browser):
    try:
        browser.get("https://api.ipify.org/?format=json")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
        print("CONNECTED TO PROXY")
    except:
        print("PROXY CONNECTION FAILED")