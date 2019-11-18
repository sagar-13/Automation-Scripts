
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from multiprocessing import Process
import unittest, time, re
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--ignore-certificate-errors')


# Easy changes for multiple people using the script
sd_path_sagar = "C:\\Users\\..." 
sd_path_nariman = "C:\\Users\\..."
sd_path_deanne = "C:\\Users\\..."

sd_path = sd_path_sagar

sagar_driver = "C:\\Users\\..."
nariman_driver = "C:\\Users\\..."
deanne_driver = "C:\\Users\\..."

driver_path = sagar_driver


def setUp():
    """This function initializes a WebDriver 
      (A Google Chrome window where everything will happen)
    
    Returns:
        driver {WebDriver}
    """
        
    driver = webdriver.Chrome(desired_capabilities=chrome_options.to_capabilities(), \
        executable_path=driver_path)
    # The application will wait 40 seconds to find something before it crashes and stops trying.
    driver.implicitly_wait(40)
    return driver
  
def LogInExt (user, password):
    """This logs into [Webpage] External

      Arguments:
          user {string} -- ***** username
          password {string} -- ***** password

      Returns:
          driver {WebDriver} -- The ***** window with the user mentioned aboved logged in
    """
    driver = setUp()
    driver.get('https://cscdqpvsdvws004.cihs.gov.on.ca:9453/*****/public/login.xhtml')
    driver.find_element_by_id('loginForm:loginName').send_keys(user)
    driver.find_element_by_id('loginForm:inputPassword').send_keys(password)
    driver.find_element_by_id('loginForm:login').click()
    driver.find_element_by_id('loginForm:password').send_keys("66")
    driver.find_element_by_id('loginForm:login').click()
    driver.find_element_by_id('dashboardForm:roleSelect').send_keys("Service Provider Admin") #use if login has multiple roles
    return driver

    

def LogInInt (user):
    """This logs into ***** Internal
    
    Arguments:
        user {string} -- ***** internal username
    
    Returns:
        driver {WebDriver} -- The ***** window with the user mentioned aboved logged in
    """
    driver = setUp()
    driver.get('https://cscdqpvsdvws004.cihs.gov.on.ca:9453/GoSecuritySimulatorWeb/Authenticate_User_files/AuthenticateUserInputLocalEPF.htm')
    driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/form/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/input').send_keys(user)
    driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/form/table/tbody/tr[2]/td/input[1]').click()
    driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[6]/td[2]/a').click()
    
    return driver

def SearchAndSelect(driver, AppID):
    """Takes a logged in internal user and navigates them to a certain licence application
    
    Arguments:
        driver {[type]} -- [description]
        AppID {[type]} -- [description]
    """
    driver.find_element_by_xpath('//*[@id="dashboardForm"]/div[2]/div[2]/h3/a/span[3]').click()
    driver.find_element_by_id("applicationMainForm:newSearch").click()
    driver.find_element_by_id("applSearchApplicationForm:applicationId").send_keys(AppID)
    driver.find_element_by_id("applSearchApplicationForm:search").click()
    driver.find_element_by_id("applSearchApplicationForm:j_id_a_4h:0:select").click()


def setProfileYJ(setProfileYJ, email):
    """Searches for the licencee profile by email and ticks the Enable YJ Profile checkbox
    
    Arguments:
        setProfileYJ {Boolean} -- True if yes, False if no
        email {String} -- licencee profile email (From the profile module)
    """

    driver = LogInInt(licensor_login)
    if setProfileYJ == True:
      setProfileYJ = 0 # 0 is the suffix of the yes button
    else: 
      setProfileYJ = 1
    
    # Log in as a licensor, search for the user profile, set it being able to/not able do YJ applications
    driver.maximize_window()
    driver.find_element_by_xpath('//*[@id="dashboardForm"]/div[2]/div[1]/h3/a/span[3]').click()
 
    driver.find_element_by_xpath('//*[@id="profileMainForm"]/div[2]/div/div/a').click()
    driver.find_element_by_id("searchUserProfileForm:email").send_keys(email)
    # driver.find_element_by_id("searchUserProfileForm:licenseeName").send_keys(name) #sometimes you may want to search by name
    
    driver.find_element_by_id("searchUserProfileForm:Search").click()
    
  
    driver.find_element_by_id("searchUserProfileForm:profileListLoop:0:j_id_34").click()

    yj = "userProfileForm:YJApp:"+ str(setProfileYJ)
    try:
      driver.find_element_by_id(yj).click()
    except NoSuchElementException:
      pass

    driver.find_element_by_id("userProfileForm:saveNext").click()
    driver.quit()


def NewLicence(applicant, prefix, suffix, Type, FundingType):
    """The external process for a New Licence Application.
    
    Arguments:
        applicant {2-Tuple} -- Contains (licencee profile email, ***** username)  
        prefix {String} -- Prefix for the name, usually specifies licence type and build number
        suffix {String} -- Suffix for the name, used to number licence applications
        Type {String} -- "CRA", "CRA-YJ", "FCA", or "Shared" 
        FundingType {String} -- Can be "TPR", "Private", or "Both"
    
    Returns:
        ID [String] -- The licence application ID
    """

    driver = LogInExt(applicant[1], "test")
    # Go to Licence Application and start a new application
    driver.find_element_by_xpath('//*[@id="dashboardForm"]/div[2]/div[2]/h2/a/span[3]').click()
    driver.find_element_by_id('applicationMainForm:newApp').click()
    driver.find_element_by_id('applNoticeForm:next').click()

    # Account for differences between types and select options accordingly
    if Type == "CRA" or Type == "CRA-YJ" or Type == "Shared" :
      driver.find_element_by_id('applLicenceTypeForm:licenceTypeRadio:0').click() #Children's residence
    
    if Type == "FCA":
      driver.find_element_by_id('applLicenceTypeForm:licenceTypeRadio:1').click() #FCA

    if Type == "CRA-YJ":
      driver.find_element_by_id('applLicenceTypeForm:youthJusticeRadio:0').click() #YJ
      driver.find_element_by_id('applLicenceTypeForm:sharedFacilityRadio:1').click() #shared
    
    if Type == "Shared":
      driver.find_element_by_id('applLicenceTypeForm:youthJusticeRadio:0').click() #YJ
      driver.find_element_by_id('applLicenceTypeForm:sharedFacilityRadio:0').click() #shared
       
    driver.find_element_by_id('applLicenceTypeForm:languagePreferRadio:0').click()

    #Sometimes FundingType is already selected so this is in a try block
    # Not sure if this is 100% correct anymore but it still works
    try:
      if FundingType == "TPR" and Type != "FCA":
        driver.find_element_by_id('applLicenceTypeForm:fundingTypeCheckbox:0').click()
      elif FundingType == "Private":
        driver.find_element_by_id('applLicenceTypeForm:fundingTypeCheckbox:1').click()
      else:
        driver.find_element_by_id('applLicenceTypeForm:fundingTypeCheckbox:0').click()
        driver.find_element_by_id('applLicenceTypeForm:fundingTypeCheckbox:1').click()
    except NoSuchElementException:
        pass

    driver.find_element_by_id('applLicenceTypeForm:licencehistQ1Radio:1').click()
    driver.find_element_by_id('applLicenceTypeForm:licencehistQ2Radio:1').click()
    driver.find_element_by_id('applLicenceTypeForm:licencehistQ3Radio:1').click()
    driver.find_element_by_id('applLicenceTypeForm:licencehistQ4Radio:1').click()
    driver.find_element_by_id('applLicenceTypeForm:licencehistQ5Radio:1').click()
    driver.find_element_by_id('applLicenceTypeForm:saveNext').click()
    driver.find_element_by_id('applApplicantInfoForm:next').click()

    #Residence information screen
    driver.find_element_by_id('applResidenceInfoForm:prefix').send_keys(prefix)
    #This just selects the first operating name in the list, you may want to select_by_visible_text or use a different index for some apps
    Select(driver.find_element_by_id('applResidenceInfoForm:operatingName')).select_by_index(1)
    driver.find_element_by_id('applResidenceInfoForm:suffix').send_keys(suffix)
    driver.find_element_by_id('applResidenceInfoForm:applicantPhoneNum').send_keys('111-111-1111')
    
    driver.find_element_by_id('applResidenceInfoForm:municipalityCity').send_keys('City of Toronto')
  
    #Again, accounting for the differences between the licence types
    if Type == "CRA" or Type == "CRA-YJ" or Type == "Shared":
      driver.find_element_by_id('applResidenceInfoForm:ownership:1').click()
      
      # You may want to use different addresses
      driver.find_element_by_id("applResidenceInfoForm:applResidenceInfoStreetType").send_keys("Mall")
      driver.find_element_by_id('applResidenceInfoForm:applResidenceInfoStreetNo').send_keys('12')
      driver.find_element_by_id('applResidenceInfoForm:applResidenceInfoStreetName').send_keys('Yonge')
      driver.find_element_by_id('applResidenceInfoForm:applResidenceInfoapplicantCityName').send_keys('toronto')
      driver.find_element_by_id('applResidenceInfoForm:applResidenceInfoapplicantPostalCode').send_keys('M2M 0A5')
      driver.find_element_by_id('applResidenceInfoForm:mailingSameAsAboveOption:0').click()
      driver.find_element_by_id('applResidenceInfoForm:drinkingWaterQ1:1').click()
      driver.find_element_by_id('applResidenceInfoForm:drinkingWaterQ2:0').click()
      driver.find_element_by_id('applResidenceInfoForm:dwisId').send_keys("5454654")
      
      driver.find_element_by_id('applResidenceInfoForm:addContact').click()

      #add contact screen
      driver.find_element_by_id('applAddContactForm:contactFirstName').send_keys('Sagar')
      driver.find_element_by_id('applAddContactForm:contactLastName').send_keys('s')
      driver.find_element_by_id('applAddContactForm:contactTitle').send_keys('Contact')
      driver.find_element_by_id('applAddContactForm:primaryPhoneNum').send_keys('(111)111-1111')
      driver.find_element_by_id('applAddContactForm:contactEmail').send_keys('narimancr@mailinator.com')
      date = datetime.datetime.today()
      driver.find_element_by_id('applAddContactForm:contactDateActivated').send_keys(date.strftime("%Y/%m/%d"))
      driver.find_element_by_id('applAddContactForm:save').click()
      driver.find_element_by_id('applAddContactForm:return').click()
      driver.find_element_by_id('applResidenceInfoForm:saveNext').click()

      #operation information screen
      driver.find_element_by_id('applOperationInfoForm:premiseDesc').send_keys("its a great place")
      driver.find_element_by_id('applOperationInfoForm:programFormat:0').click()
      driver.find_element_by_id("applOperationInfoForm:programDesc").send_keys("its a great program")
      driver.find_element_by_id("applOperationInfoForm:ageRange:0").click()
      driver.find_element_by_id("applOperationInfoForm:gender:0").click()
      driver.find_element_by_id("applOperationInfoForm:serviceCategoryRadioCR_0").click()
      driver.find_element_by_id("applOperationInfoForm:j_id_a_l_1l_1_2_1").click()
      driver.find_element_by_id("applOperationInfoForm:capacity").send_keys("20") #proposed capacity
      driver.find_element_by_id("applOperationInfoForm:addRoom").click()
      
      #room information
      driver.find_element_by_id("applRoomInfoForm:roomName").send_keys("Room1")
      driver.find_element_by_id("applRoomInfoForm:roomSizeMeasurement:0").click()
      driver.find_element_by_id("applRoomInfoForm:roomSizeWidth").send_keys("100")
      driver.find_element_by_id("applRoomInfoForm:roomSizeLength").send_keys("100")
      driver.find_element_by_id("applRoomInfoForm:bedNo").send_keys("20") # number of beds
      driver.find_element_by_id("applRoomInfoForm:ageRange:0").click()
      driver.find_element_by_id("applRoomInfoForm:gender:0").click()
      driver.find_element_by_id("applRoomInfoForm:floor").send_keys("First")
      driver.find_element_by_id("applRoomInfoForm:save").click()
      driver.find_element_by_id("applRoomInfoForm:return").click()
      driver.find_element_by_id("applOperationInfoForm:saveNext").click()
     
      #Upload zoning approval document
      driver.find_element_by_xpath('//*[@id="mandatorySuppDocTable"]/div/div[2]/div/div[7]/div/a').click()
      driver.find_element_by_id("applUploadSupportingDocsForm:comments").send_keys("SD")
      driver.find_element_by_id("applUploadSupportingDocsForm:uploadedFile").send_keys(sd_path)
      driver.find_element_by_id("applUploadSupportingDocsForm:save").click()
      
      driver.find_element_by_id("applUploadSupportingDocsForm:return").click()
    

      # Uploading supporting documents isnt really necessary other than Zoning approval
 
      # for i in range(0,50):
      #   s1= Select(driver.find_element_by_id('applSupportingDocsForm:otherMandatoryDocumentsappItemsPerPage'))
      #   index = len(s1.options)
      #   s1.select_by_index(index - 1)
      #   try : 
      #     button = "applSupportingDocsForm:j_id_a_j_1_1_s_1_" + str(i) + "_h_1_3"
      #     # button = "applSupportingDocsForm:j_id_a_k_1_1_s_1_" + str(i) + "_h_1_3"            
      #     driver.find_element_by_id(button).click()
      #     driver.find_element_by_id("applUploadSupportingDocsForm:uploadedFile").send_keys(sd_path)
      #     driver.find_element_by_id("applUploadSupportingDocsForm:save").click()
      #     
      #     driver.find_element_by_id("applUploadSupportingDocsForm:return").click()
          
      #   except NoSuchElementException:
      #     break

      
      driver.find_element_by_id("applSupportingDocsForm:uploadFile").click() # (additional document)
      driver.find_element_by_id("applUploadSupportingDocsForm:otherDocumentTypeDesc").send_keys("additionaldoc")
      driver.find_element_by_id("applUploadSupportingDocsForm:uploadedFile").send_keys(sd_path)
      driver.find_element_by_id("applUploadSupportingDocsForm:save").click()
      
      driver.find_element_by_id("applUploadSupportingDocsForm:return").click()
      

      driver.find_element_by_id("applSupportingDocsForm:next").click()
      # Submit
      driver.find_element_by_id("applApplicationSummaryForm:submit").click()
      driver.switch_to.alert.accept()

      #declaration
      driver.find_element_by_id('applDeclarationConsentForm:consent:0').click()
      driver.find_element_by_id('applDeclarationConsentForm:attestation:0').click()
      
      driver.find_element_by_id('applDeclarationConsentForm:submit').click()

    # FCA  
    else:
      
      driver.find_element_by_id('applResidenceInfoForm:mailingSameAsAboveOptionFC:0').click()
      
      driver.find_element_by_id('applResidenceInfoForm:addAddress').click()
      
      driver.find_element_by_id('applAddAddressForm:officeMunicipality').send_keys('City of Toronto')
      

      driver.find_element_by_id('applAddAddressForm:officeStreetNo').send_keys('13')
      driver.find_element_by_id('applAddAddressForm:officeStreetName').send_keys('Andrew')
      driver.find_element_by_id('applAddAddressForm:officeStreetType').send_keys('Street') 
      driver.find_element_by_id('applAddAddressForm:officeapplicantCityName').send_keys('Brampton')
      driver.find_element_by_id('applAddAddressForm:officeapplicantPostalCode').send_keys('M2M 8T4')
      driver.find_element_by_id('applAddAddressForm:primaryPhoneNum').send_keys('222-111-1111')
      driver.find_element_by_id('applAddAddressForm:isLeadOffice:0').click()
      driver.find_element_by_id('applAddAddressForm:save').click()
      driver.find_element_by_id('applAddAddressForm:return').click()
      driver.find_element_by_id('applResidenceInfoForm:saveNext').click()
      
      #operation information screen
      driver.find_element_by_id('applOperationInfoForm:fcaNo').send_keys("1")
      driver.find_element_by_id('applOperationInfoForm:fccNo').send_keys("10")
      driver.find_element_by_id("applOperationInfoForm:fcaUtilization").send_keys("its a great program")
      driver.find_element_by_id("applOperationInfoForm:serviceCategoryRadio_0").click()
      driver.find_element_by_id("applOperationInfoForm:saveNext").click()
      
      # Uploading supporting documents isnt really necessary other than Zoning approval
      for i in range(0,50):
        s1= Select(driver.find_element_by_id('applSupportingDocsForm:otherMandatoryDocumentsappItemsPerPage'))
        index = len(s1.options)
        s1.select_by_index(index - 1)
        try :
          button = "applSupportingDocsForm:j_id_a_k_1_1_s_1_" + str(i) + "_h_1_3"            
          driver.find_element_by_id(button).click()
          driver.find_element_by_id("applUploadSupportingDocsForm:uploadedFile").send_keys(sd_path)
          driver.find_element_by_id("applUploadSupportingDocsForm:save").click()
          
          driver.find_element_by_id("applUploadSupportingDocsForm:return").click()
          
        except NoSuchElementException:
          break
      
      driver.find_element_by_id("applSupportingDocsForm:uploadFile").click() # (additional document)
      driver.find_element_by_id("applUploadSupportingDocsForm:otherDocumentTypeDesc").send_keys("additionaldoc")
      driver.find_element_by_id("applUploadSupportingDocsForm:uploadedFile").send_keys(sd_path)
      driver.find_element_by_id("applUploadSupportingDocsForm:save").click()
      
      driver.find_element_by_id("applUploadSupportingDocsForm:return").click()

      driver.find_element_by_id("applSupportingDocsForm:next").click()
      
      #SO report summary screen
      driver.find_element_by_id("applApplicationSummaryForm:submit").click()
      
      driver.switch_to.alert.accept()
      driver.find_element_by_id("applDeclarationConsentForm:fcaConsent:0").click()
      
      driver.find_element_by_id("applDeclarationConsentForm:consent:0").click()
      
      driver.find_element_by_id("applDeclarationConsentForm:attestation:0").click()
      
      driver.find_element_by_id("applDeclarationConsentForm:submit").click()
      

    # Prints application ID and goes back to ***** Dashboard
    element = driver.find_element_by_xpath('//*[@id="applConfirmationForm"]/div/div/div[2]/div')
    # Parsing the tombstone for the application ID
    ID = element.text[15:].rstrip()
    print(ID)
    driver.find_element_by_xpath('//*[@id="moduleHeader"]/div/div/ol/li[1]/a').click()
    driver.quit()
    return ID

def NewLicence_lm(AppID):
    """The first step of the internal process, Under Licening Manager for Assignment
    
    Arguments:
        AppID {String} -- The ID of the externally submitted Licence App
    """
    # Log in, search for the ID, and select it
    driver = LogInInt(lm_login)
    SearchAndSelect(driver, AppID)

    # Head to Ministry Action, and submit after assigning the licensor and program supervisor
    driver.find_element_by_xpath('//*[@id="applTabs"]/div[2]/div[4]/a').click()
    
    driver.find_element_by_id("applMinistryActionForm:nextStep").send_keys("Submit for Program Supervisor review")
    Select(driver.find_element_by_id("applMinistryActionForm:managerPA")).select_by_visible_text(licensor_name)
    Select(driver.find_element_by_id("applMinistryActionForm:managerPS")).select_by_visible_text(ps_name)
   
    
    driver.find_element_by_id("applMinistryActionForm:applicationMinistryActionSubmit").click()
    
    driver.switch_to.alert.accept()
    
    driver.quit()

def NewLicence_ps(AppID, Type):
    """The second step of the internal process, Under Program Supervisor Review
    
    Arguments:
        AppID {String} -- The ID of the externally submitted Licence App
        Type {String} -- The Licence Type

    """
    # Log in and select the Program Supervisor Role from the dashboard
    driver = LogInInt(ps_login)
    Select(driver.find_element_by_id('dashboardForm:j_id_e_9')).select_by_value("PS")
    SearchAndSelect(driver, AppID)

    # Go to ministry action, upload the rate letter
    driver.find_element_by_xpath('//*[@id="applTabs"]/div[2]/div[4]/a').click()
    driver.find_element_by_id('applMinistryActionForm:j_id_a_4v_g:0:buttonUpload').click()
    driver.find_element_by_id("applUploadAttachmentForm:uploadedFile").send_keys(sd_path)
    driver.find_element_by_id("applUploadAttachmentForm:save").click()
    driver.find_element_by_id("applUploadAttachmentForm:return").click()
    
    # Leave some notes and submit to licensor
    driver.find_element_by_id("applMinistryActionForm:nextStep").send_keys("Initial review completed")
    
    driver.find_element_by_id("applMinistryActionForm:internalNotes").send_keys("initial review was great")
    
    driver.find_element_by_id("applMinistryActionForm:applicationMinistryActionSubmit").click()
    
    driver.switch_to.alert.accept()
    
    driver.quit()

    
def NewLicence_pa(AppID, Type, expiry_date, InspectionComplete):
    """The third step of the internal process. Under Licensor Review
    
    Arguments:
        AppID {String} -- The ID of the externally submitted Licence App
        Type {String} -- The Licence Type
        expiry_date {String} -- The expiry date to be specified on Ministry Action
        InspectionComplete {Boolean} -- Inspection already done or not? 
    """

    driver = LogInInt(licensor_login)
    SearchAndSelect(driver, AppID)

    # Supporting Documents
    driver.find_element_by_xpath('//*[@id="applTabs"]/div[1]/div[2]/a').click()

    #mandatory documents prior to submission
    if Type != "FCA":
      # zoning approval                              
      driver.find_element_by_xpath('//*[@id="applSupportingDocumentForm:j_id_a_e_1_v_1_0_h_5"]').click()
                                    
      currentStatus = driver.find_element_by_id("applSummarySupportingDocsForm:currentStatus")
      if currentStatus.text.lower() in ['not required', 'satisfactory']:
          driver.find_element_by_id('applSummarySupportingDocsForm:cancel').click() # Cancel if it's already good
          
      else:
        driver.find_element_by_id('applSummarySupportingDocsForm:nextStep').send_keys("Satisfactory") # Mark as satisfactory and submit
        
        driver.find_element_by_id('applSummarySupportingDocsForm:submit').click()     

    
    #The big list of supporting documents
    for i in range(0, 50):
          

      # Currently the pagination resets to 10 per page, so after every document, we have to select the highest option again
      s1= Select(driver.find_element_by_id('applSupportingDocumentForm:otherMandatoryDocumentsPerPage'))
      index = len(s1.options)
      s1.select_by_index(index - 1)

      # Check the status of a supporting document before clicking into it
      try:
        status = '//*[@id="otherMandatorySuppDocTable"]/div/div[2]/div[' + str(i + 1) +  ']/div[4]'
        doc_status = driver.find_element_by_xpath(status).text.lower()
        if doc_status in ['not required', 'satisfactory']:
          continue

        button = "applSupportingDocumentForm:j_id_a_f_1_s_1_"+ str(i) +"_h_5"             
        driver.find_element_by_id(button).click()
      except NoSuchElementException:
        break # Leaves the for loop if a button can't be clicked anymore

      # Supporting documents subpage     
      docType = driver.find_element_by_id("currentDocType")  
      currentStatus = driver.find_element_by_id("applSummarySupportingDocsForm:currentStatus")

      # Don't need this anymore since it's handled above but keeping it for now
      # if currentStatus.text.lower() in ['not required', 'satisfactory']:
      #   driver.find_element_by_id('applSummarySupportingDocsForm:cancel').click()
      #   
      # else:
      
      # Profile document
      if "Operator suitability" in docType.text:
        driver.find_element_by_id('applSummarySupportingDocsForm:nextStep').send_keys("Satisfactory")
      # Regular document
      else:
        driver.find_element_by_id('applSummarySupportingDocsForm:nextStep').send_keys("Not required")
        driver.find_element_by_id('applSummarySupportingDocsForm:notRequiredNotes').send_keys("N/A")
      driver.find_element_by_id('applSummarySupportingDocsForm:submit').click()  
    
    # Submit for Licensing manager
    if Type == "FCA" or InspectionComplete:
      
      driver.find_element_by_xpath('//*[@id="applTabs"]/div[2]/div[4]/a').click()
      driver.find_element_by_id("applMinistryActionForm:nextStep").send_keys("Submit for Licensing Manager review")
      
      driver.find_element_by_id("applMinistryActionForm:recommendationOption:0").click()
      
      driver.find_element_by_id("applMinistryActionForm:expiryDate").send_keys(expiry_date)
      
      driver.find_element_by_id("applMinistryActionForm:applicationMinistryActionSubmit").click()
      
      driver.switch_to.alert.accept()
      
      driver.quit()



    
def NewLicence_lm_2(AppID, Type):
    """The fourth step of the internal licensing application process,
    Under Licensing Manager Review
    
    Arguments:
        AppID {String} -- The ID of the externally submitted Licence App
        Type {String} -- The Licence Type
        
    """
    driver = LogInInt("qa_lm_to")
    SearchAndSelect(driver, AppID)

    # Straight to Ministry Action
    driver.find_element_by_xpath('//*[@id="applTabs"]/div[2]/div[4]/a').click()
   
    # CRA/FCA can approve but CRA-YJ and Shared must go to regional manager
    if Type == "CRA" or Type == "FCA":
      driver.find_element_by_id("applMinistryActionForm:nextStep").send_keys("Approve")
      
    else:
      driver.find_element_by_id("applMinistryActionForm:nextStep").send_keys("Submit for Regional Manager Review")
      
    
    # Submit
    driver.find_element_by_id("applMinistryActionForm:applicationMinistryActionSubmit").click()
    
    driver.switch_to.alert.accept()
    
     
    driver.quit()
    
def NewLicence_rm(AppID):
    """The fifth step of the internal licensing application process,
    Under Regional Manager Review
    
    Arguments:
        AppID {String} -- The ID of the externally submitted Licence App
        
    """
    driver = LogInInt("qa_rm_to")
    SearchAndSelect(driver, AppID)

    #Ministry Action, Approve, Submit
    driver.find_element_by_xpath('//*[@id="applTabs"]/div[2]/div[4]/a').click()
    
    driver.find_element_by_id("applMinistryActionForm:nextStep").send_keys("Approve")
    
    driver.find_element_by_id("applMinistryActionForm:applicationMinistryActionSubmit").click()
    
    driver.switch_to.alert.accept()
    
    driver.quit()
 
#, ps_name , ps_login, licensor_name, licensor_login, lm_login, ID = ""):
def Create_Licence(applicant, prefix, suffix, Type, expiry_date, FundingType, ID =""): 
    """This function calls of the above functions to form the complete licence application process
    
    Arguments:
        applicant {2-Tuple} -- (licencee profile email, ***** username) combo
        prefix {String} -- Prefix for the name, usually specifies licence type and build number
        suffix {String} -- Suffix for the name, used to number licence applications
        Type {String} -- "CRA", "CRA-YJ", "FCA", or "Shared" 
        expiry_date {String} -- The expiry date to be provided on the Ministry Action screen
        FundingType {String} -- Can be "TPR", "Private", or "Both"

    Optional Arguments:
        ID {String} -- if this is provided, the external process is skipped (default: {""})
                      Also, the only parameters that matter then are expiry_date and Type

    """
    if ID == "":
      if Type == "CRA-YJ" or Type == "Shared":
        setProfileYJ(True, applicant[0])
      ID = NewLicence(applicant, prefix, suffix, Type, FundingType)
      
    NewLicence_lm(ID)
    NewLicence_ps(ID, Type)
    NewLicence_pa(ID, Type, expiry_date, False) # The False is to show inspection will not done, don't change this.
   
    if Type == "CRA-YJ" or Type == "Shared":
        NewLicence_lm_2(ID, Type)
        NewLicence_rm(ID)
    else:      
      NewLicence_lm_2(ID, Type)

""" 
This function is ran when inspection is done. 
True is passed into NewLicence_pa to indicate the inspection is complete

"""
def post_inspection(ID, Type, expiryDate):
    NewLicence_pa(ID, Type, expiry_date, True)  
    if Type == "CRA-YJ" or Type == "Shared":
        NewLicence_lm_2(ID, Type)
        NewLicence_rm(ID)
    else:      
      NewLicence_lm_2(ID, Type)

      
   
def multi_process(process_args):
    """Takes a list of lists of arguments for Create_Licence and executes applications in parallel
    
    Arguments:
        process_args {List of lists} -- Each list should contain args for Create_Licence
    """
    processes = []
    # Creates a bunch of "plans" and adds them to a list, and starts them.
    for arg_list in process_args:
      p = Process(target=Create_Licence, args = arg_list)
      processes.append(p)
      p.start()
    # Synchronize the plans
    for p in processes:
      p.join()

# Creates a list of n Create_Licence arguments of the same type for use with multiprocess
def Create_N_Licences(applicant, prefix, Type, expiry_date, FundingType, n, expiry_dates = []):
  Licence_List = []
  for i in range(1, n+1):
    if expiry_dates != []:
      expiry_date = expiry_dates[i-1]
    
    licence = [applicant, prefix, str(i), Type, expiry_date, FundingType]
    Licence_List.append(licence)
  # return licence_list
  multi_process(Licence_List)


#important info for the app, these variables could be added as function parameters in Create_Licence for convenience if 
# they are changed in the future. Could be usefulwhen creating data for multiple people with different ps, pa, and lm 
# at the same time. For most use cases, these can be global.

# Names are lastname, firstname
lm_login = "qa_lm_to"
ps_name = "QA Lansdowne, QA Eir"
ps_login = "qa_ps_to"
licensor_name = "QA Jane, QA Hrid"
licensor_login = "qa_pa_to"

if __name__ == "__main__":   
    int_roles = [ps_name , ps_login, licensor_name, licensor_login, lm_login]
  
    #This will get today's date in the format of the date pickers
    date = datetime.datetime.today()
    expiry = date + datetime.timedelta(days=60)
    expiry_date = expiry.strftime("%Y/%m/%d")
    # You could also just enter it manually:
    # expiry_date = "2019/11/15"

    # Name your prefix  
    prefix = "Sagar_1.54_" 

    # This just attaches the licence type in front of the prefix 
    CRA, YJ, FCA, Shared = "CRA_" + prefix, "YJ_" + prefix, "FCA_" + prefix, "Shared_" + prefix
     

    # Add your applicants here
    # (Licencee profile email, username for login)
    qa145 = ("joyce_ind.*****@mailinator.com", "ru_test_145")
    qa45 = ("qa_ru_045@mailinator.com", "qa_ru_045")
    ind = ("nariman141@mailinator.com", "sagar_datacreation@mailinator.com")
    
    #Assign the right applicant
    applicant = qa45
    
    


    #### Example usage of Create_Licence
    Create_Licence(applicant, FCA, "1", "FCA", expiry_date,"Both" ) 
    # Create_Licence(applicant, Shared, "1", "Shared", expiry_date, "Both",) 


    #### Example usage of multi-process
    # a = [jane_corp, FCA, "3", "FCA", '08/24/2020', "Both" ]
    # b = [jane_ind, FCA, "4", "FCA", '08/24/2020', "Both" ]
    # list1.append(a)
    # list1.apppend(b)
    # multi_process([a,b])
    # Create_N_Licences()

    #### Example usage of Create_N_Licences
    # Create_N_Licences(applicant, FCA, "FCA", expiry_date, "Both", 3, ['08/30/2019', '9/30/2019', '8/24/2020'])
    # Create_N_Licences(applicant, FCA, "FCA", expiry_date, "Both", 10)




   
        

   

