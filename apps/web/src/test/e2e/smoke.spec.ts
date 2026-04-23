import { expect, test } from '@playwright/test'

test('experience flow smoke', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('fixture-grid')).toBeVisible()
  await page.getByRole('button', { name: /从 fixture 进入|Enter via fixture/i }).click()

  await expect(page.getByTestId('observatory-section')).toBeVisible()
  await page.locator('.branch-chip').nth(1).click()
  await page.locator('[data-testid="intervention-section"] textarea').fill('Create a visible intervention that redistributes cost.')
  await page.getByRole('button', { name: /Run Replay/i }).click()
  await expect(page.getByTestId('ripple-section')).toBeVisible()

  await page.getByRole('button', { name: /Generate Share Text/i }).click()
  await page.getByRole('button', { name: /Open Calibration|Hide Calibration/i }).click()
  await expect(page.getByTestId('calibration-drawer')).toBeVisible()
  await page.getByTestId('calibration-drawer').locator('textarea').fill('The audience response split into two visible camps.')
  await page.getByRole('button', { name: /Save Calibration/i }).click()
  await expect(page.getByRole('button', { name: /Open Calibration/i })).toBeVisible()
})
