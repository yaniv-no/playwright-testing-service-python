# init testing 
npm init @azure/microsoft-playwright-testing@latest

# create env variables
export PLAYWRIGHT_SERVICE_URL='wss://westeurope.api.playwright.microsoft.com/accounts/westeurope_05717352-de09-4143-8c31-26d1520c604a/browsers'

#for remote testing 
export AZURE_FUNCTIONAPP_URL='https://playwright-testing-service-python-cxhfe9g7faachrd7.swedencentral-01.azurewebsites.net'

#run tests
npx playwright test --config=playwright.service.config.ts --workers=20