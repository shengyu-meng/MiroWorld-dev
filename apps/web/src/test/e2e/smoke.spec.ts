import { expect, test } from '@playwright/test'

test('experience flow smoke', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('fixture-grid')).toBeVisible()
  await page.getByRole('button', { name: /从 fixture 进入|Enter via fixture/i }).click()

  await expect(page.getByTestId('observatory-section')).toBeVisible()
  await page.locator('.branch-chip').nth(1).click()
  await page.getByRole('button', { name: /Intervention/i }).click()
  await page.locator('[data-testid="intervention-section"] textarea').fill('Create a visible intervention that redistributes cost.')
  await page.getByRole('button', { name: /运行重演|Run Replay/i }).click()
  await expect(page.getByTestId('ripple-section')).toBeVisible()

  await page.getByRole('button', { name: /Archive/i }).click()
  await expect(page.getByTestId('archive-section')).toBeVisible()
  await page.getByRole('button', { name: /生成分享文本|Generate Share Text/i }).click()
  await page.getByRole('button', { name: /打开校准|收起校准|Open Calibration|Hide Calibration/i }).click()
  await expect(page.getByTestId('calibration-drawer')).toBeVisible()
  await page.getByTestId('calibration-drawer').locator('textarea').fill('The audience response split into two visible camps.')
  await page.getByRole('button', { name: /保存校准|Save Calibration/i }).click()
  await expect(page.getByRole('button', { name: /打开校准|Open Calibration/i })).toBeVisible()
})
