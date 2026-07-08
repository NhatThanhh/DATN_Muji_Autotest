# Automated Web Testing Framework 
## Project Overview

Built an automated testing framework for the MUJI Vietnam website and integrated it into a CI/CD pipeline.  
The project also applied AI-assisted tools, including GitHub Copilot and Playwright MCP, to support test script generation and evaluate the level of AI support in automated software testing.

## Test Cases

The test cases file is stored in `test_cases/Muji_Test_Case.xlsx`.

## Technologies Used

- Python
- Playwright
- Pytest
- Page Object Model (POM)
- Allure Report
- GitHub Actions
- GitHub Copilot
- Playwright MCP

## Tested Website

- Website: MUJI Vietnam
- URL: https://www.muji.com.vn/vn

## Main Features Tested

- User registration
- User login
- Product search

## Key Implementations

### Page Object Model

The framework applies the Page Object Model to separate page locators, page actions and test logic.  
This helps improve code readability, maintainability and reusability.

### Data-Driven Testing

Test data is stored in JSON files in test_data folder to support multiple test scenarios, including valid, invalid and negative cases.

### CI/CD Integration

GitHub Actions is configured to run automated tests when changes are pushed to the repository.  

### AI-Assisted Test Script Generation

GitHub Copilot and Playwright MCP are used to support test script generation.  
The project evaluates how AI tools can assist in creating locators, page objects and automated test scripts based on the actual website interface.

The testing framework and test scripts generated with AI assistance are stored in a separate repository to support CI/CD integration using GitHub Actions.

**AI-Assisted Testing Repository:** https://github.com/NhatThanhh/Copilot_PlaywrightMCP_autotest
## Installation

### 1. Clone the repository

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

## Running Tests

Run all tests:

```bash
pytest
```

Run tests and generate Allure results:

```bash
pytest --alluredir=reports/allure-results
```

## Project Purpose

This project aims to:

- Build a maintainable automated web testing framework.
- Apply Playwright and Pytest for functional testing.
- Use the Page Object Model to improve test code structure and maintainability.
- Use Allure Report for clear test result visualization.
- Integrate automated testing into a CI/CD pipeline.
- Evaluate the effectiveness of AI-assisted test script generation in automated software testing.
