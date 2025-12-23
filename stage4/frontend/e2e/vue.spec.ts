import { test, expect } from '@playwright/test'

test('visits the app root url', async ({ page }) => {
  await page.goto('/')
  await expect(page.locator('h1')).toHaveText('Search Courses')
  await page.getByPlaceholder('Enter a course or keyword (e.g. python, web, UX)').fill('python')
  await page.getByRole('button', { name: 'Search' }).click()
  await expect(page.getByText('Python for Data Analysis')).toBeVisible()
})
