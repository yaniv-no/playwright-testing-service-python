# Flask on Azure Function Example

This project is a simple Python web application using Flask, served via Azure Functions. It displays an HTML page with two buttons. The project includes GitHub Actions workflows for deployment and Playwright-based testing using Azure Playwright Testing Service.

## Structure
- `FlaskApp/flask_app.py`: Main Flask app, Azure Function entry point
- `FunctionApp/function.json`: Azure Functions binding configuration
- `requirements.txt`: Python dependencies
- `.github/workflows/azure-deploy-and-test.yml`: CI/CD pipeline for deployment and testing
- `tests/`: Playwright test folder

## Setup
1. Set up your Azure Function App and Playwright Testing Service.
2. Add the following secrets to your GitHub repository:
   - `AZURE_FUNCTIONAPP_NAME`
   - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
   - `AZURE_FUNCTIONAPP_URL`
   - `AZURE_PLAYWRIGHT_SERVICE_CONNECTION`
3. Push to `main` to trigger deployment and tests.

## Local Development
```bash
python3 -m venv venv # create a virtual environment
source venv/bin/activate # activate the virtual environment
pip3 install -r requirements.txt # download dependencies
```
# Run locally (for development only)
python3 app.py
```

## Notes
- The Playwright test is a placeholder. Update the URL and selectors as needed.
- The workflow expects your Azure resources and secrets to be set up in advance.
