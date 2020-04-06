from selenium.webdriver.common.by import By


class BaseLocators:
    pass


class MainPageLocators(BaseLocators):
    AUTHORIZATION = (By.XPATH, '//div[@class="responseHead-module-button-1BMAy4"]')
    LOGIN_FRAME = (By.XPATH, '//div[@class="authForm-module-wrap-3k5LUW"]')
    LOGIN_INPUT = (By.XPATH,
                   '//input[@class="authForm-module-input-9t5W5U input-module-input-1xGLR8"]')
    PASSWORD_INPUT = (By.XPATH,
                      '//input[@class="authForm-module-inputPassword-2Atq4Q input-module-input-1xGLR8"]')
    ENTER_TO_CABINET = (By.XPATH, '//div[@class="authForm-module-button-2G6lZu"]')


class CampaignsPageLocators(BaseLocators):
    USERNAME_WRAP = (By.XPATH, '//div[@class="right-module-userNameWrap-34ibLS"]')
    CAMPAIGNS_NEW = (By.XPATH, '//div[@class="empty-table-data-message js-main-view-no-campaigns-msg"]//'
                               'a[@href="/campaign/new"]')
    AUDIENCE_PAGE = (By.XPATH, '//a[@class="center-module-button-cQDNvq center-module-segments-3y1hDo"]')
    ACTIVE_TRAFFIC_ITEM = (By.XPATH, '//div[@class="column-list-item _traffic"]')
    INPUT_LINK_FIELD = (By.XPATH, '//div[@class="input input_create-main-url"]//'
                                  'input[@class="input__inp js-form-element"]')
    INPUT_NAME_FIELD = (By.XPATH, '//div[@class="campaign-name__name-wrap js-campaign-name-wrap"]//'
                                  'div[@class="input input_campaign-name input_with-close"]//'
                                  'input[@class="input__inp js-form-element"]')
    BANNER_SLOT = (By.XPATH, '//div[@class=" js-banner-formats-wrap"]//div[@id="192"]')
    UPLOAD_IMAGE_BUTTON = (By.XPATH, '//div[@class="input__upload-wrap js-input-upload-wrap"]//'
                                     'button[@class="button button_general"]')
    UPLOAD_IMAGE = (By.XPATH, '//input[@data-gtm-id="load_image_btn_240_400"]')
    SUBMIT_ADVERTISEMENT = (By.XPATH, '//div[@class="banner-form__footer js-footer-wrap"]//'
                                      'button[@class="button button_submit"]')
    SAVE_BUTTON = (By.XPATH, '//div[@class="js-save-button-wrap"]//button[@class="button button_submit"]')
    LAST_CAMPAIGN_NAME = (By.XPATH, '//table[@class="flexi-table-nt__tbl-tbody js-child-table"]//'
                                    'tr[1]//a[@class="campaigns-tbl-cell__campaign-name"]')
    CREATE_CAMPAIGN_MAIN = (By.XPATH, '//a[@class="campaigns-tbl-settings__button '
                                      'campaigns-tbl-settings__button_new"]')


class LoginPageLocators(BaseLocators):
    INVALID_LOGIN_OR_PASSWORD = (By.XPATH, '//div[@class="formMsg js_form_msg"]//div[@class="formMsg_text"]')


class AudiencePageLocators(BaseLocators):
    CREATE_NEW_SEGMENT = (By.XPATH, '//a[@href="/segments/segments_list/new"]')
    CREATE_SEGMENT = (By.XPATH, '//div[@class="segments-list__btn-wrap js-create-button-wrap"]/'
                                'button[@class="button button_submit"]')
    CREATE_SEGMENT_BUTTON = (By.XPATH, '//div[@class="create-segment-form__block create-segment-form_'
                                       '_block_add js-add-segments-button"]')
    PLAY_AND_PAY_CHECKBOX = (By.XPATH, '//input[@class="adding-segments-source__checkbox js-main-source-checkbox"]')
    SUBMIT_SEGMENT_BUTTON = (By.XPATH, '//div[@class="adding-segments-modal__btn-wrap js-add-button"]//'
                                       'button[@class="button button_submit"]')
    SUBMIT_ALL_SEGMENT_BUTTON = (By.XPATH, '//div[@class="create-segment-form__btn-wrap js-create-segment-'
                                           'button-wrap"]/button[@class="button button_submit"]')
    INPUT_CREATE_SEGMENT_FORM = (By.XPATH, '//div[@class="input input_create-segment-form"]/'
                                           'div[@class="input__wrap"]/'
                                           'input[@class="input__inp js-form-element"]')
    SEGMENT_NAME = (By.XPATH, '//table[@class="flexi-table__tbl js-table"]//tbody[@class="js-rows"]//tr[last()]//'
                              'a[@class="adv-camp-cell adv-camp-cell_name"]')
    DELETE_SEGMENT = (By.XPATH, '//table[@class="flexi-table__tbl js-table"]//tbody[@class="js-rows"]//tr[last()]//'
                                'div[@data-class-name="RemoveView"]')
    DELETE_BUTTON = (By.XPATH, '//button[@class="button button_confirm-remove button_general"]')
    OK_AND_MOY_MIR_1 = (By.XPATH, '//div[@class="adding-segments-modal__block-left js-sources-types"]//'
                                'div[@class="adding-segments-item"]')
    'adding-segments-item adding-segments-item_active'
    OK_AND_MOY_MIR_2 = (By.XPATH, '//div[@class="adding-segments-modal__block-left js-sources-types"]//'
                                'div[@class="adding-segments-item adding-segments-item_active"]')
