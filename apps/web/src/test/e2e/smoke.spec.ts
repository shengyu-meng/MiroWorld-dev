import { expect, test } from '@playwright/test'

test('viewer can unfold a worldline without writing an intervention', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('fixture-grid')).toBeVisible()
  await page.locator('.fixture-card').first().click()
  await page.locator('.primary-action').click()

  await expect(page.getByTestId('worldline-theatre')).toBeVisible()
  await expect(page.getByTestId('revealed-event-count')).toContainText(/1 \/ 3|1 \/ 4|1 \/ 5/)
  await expect(page.getByTestId('process-trace-panel')).toBeVisible()
  await expect(page.getByTestId('process-file-path')).toContainText(/data\/runtime\/process/)

  await page.getByTestId('worldline-next').click()
  await expect(page.getByTestId('progressive-worldline').locator('li').nth(1)).toBeVisible()
  await expect(page.getByTestId('process-trace-panel')).toBeVisible()

  await page.getByTestId('worldline-next').click()
  await expect(page.getByTestId('progressive-worldline').locator('li').nth(2)).toBeVisible()

  await page.getByTestId('worldline-next').click()
  await expect(page.getByTestId('archive-section')).toBeVisible()
  await expect(page.getByTestId('archive-terminal')).toBeVisible()
})
