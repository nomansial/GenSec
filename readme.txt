1. Install stable version of python from https://www.python.org/downloads/
2. Im using python version 3.12 I would recommend you install same version.
3. Verify pyhon installation by running command python --version in windows cmd tool.
4. Download Allure report zip file from repository https://github.com/allure-framework/allure2/releases
5. Unzip allure zip folder and add path to windows directory
6. Verify allure installation by running command allure --version in windows cmd
7. Install pycharm community edition version 2024.3.2
8. Open pycharm and import project from github.
9. Install all the libraries. Just bring mouse cursor over import in any .py file and it will show option to install the dependencies.

10. Once everything is ready add API keys in properties.ini files as shown in screenshot in email.

11. Run below command ini pycharm terminal to run all the API test cases:


behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results; allure generate reports/allure-results -o reports/allure-report --clean; allure open reports/allure-report


12. If you want to run any single API then replace feature file name in below command and run it:

behave features/Update_API_Information_of_an_existing_chatbot.feature --no-capture --tags=Test --format=pretty