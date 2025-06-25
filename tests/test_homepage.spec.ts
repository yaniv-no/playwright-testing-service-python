// Playwright test for Azure Playwright Testing Service
// Replace 'https://REPLACE_WITH_FUNCTION_URL' with your deployed function URL

import { test, expect } from '@playwright/test';
import * as dotenv from 'dotenv';
dotenv.config();

test('homepage', async ({ page }) => {
  const url = process.env.AZURE_FUNCTIONAPP_URL;
  if (!url) throw new Error('AZURE_FUNCTIONAPP_URL environment variable is not set');
  await page.goto(url);
  await expect(page.getByText('Welcome to Flask on Azure Function!')).toBeVisible();
  await page.click('text=Button 1');
  await page.click('text=Button 2');
});
