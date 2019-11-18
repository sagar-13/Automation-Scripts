# Automation-Scripts

A side project to improve efficiency during my internship.
Note: Any potentially sensitive information has been removed or edited out. 


In this project, I used Selenium to automate a lengthy data-creation process. 
This allowed anyone in any team (development or QA) to create their own data 
on their own machine (Selenium is open-source and free).

Prior to this, the data creation scripts in use were only accessible by the automation team 
as they were created with UFT (paid software) which was only installed on a few machines. 
Additionally, the execution time of those scripts was very slow. 


The new scripts ended up being a lot faster due to how quick Selenium's webdriver operates. 
Additionally, I also implemented multi-processing to run many instances of the script simultaneously. 
This allowed creation of massive amounts of unique data simultaenously (Especially on the higher-spec
computers).
