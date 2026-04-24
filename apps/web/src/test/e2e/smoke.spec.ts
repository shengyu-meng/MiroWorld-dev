import { expect, test } from '@playwright/test'

test('viewer can unfold a worldline without writing an intervention', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('fixture-grid')).toBeVisible()
  await page.locator('.fixture-card').first().click()
  await page.locator('.primary-action').click()

  await expect(page.getByTestId('worldline-theatre')).toBeVisible()
  await expect(page.getByTestId('revealed-event-count')).toContainText(/1 \/ 3|1 \/ 4|1 \/ 5/)
  await expect(page.getByTestId('theatre-readout')).toContainText(/1 \/ 3|1 \/ 4|1 \/ 5/)
  await expect(page.getByTestId('stage-orbit-map')).toBeVisible()
  await expect(page.getByTestId('process-trace-panel')).toBeVisible()
  await expect(page.getByTestId('process-file-path')).toContainText(/data\/runtime\/process/)

  await page.getByTestId('worldline-next').click()
  await expect(page.getByTestId('progressive-worldline').locator('li').nth(1)).toBeVisible()
  await expect(page.getByTestId('progress-save-state')).toContainText(/saved|已保存/i)
  await page.reload()
  await expect(page.getByTestId('worldline-theatre')).toBeVisible()
  await expect(page.getByTestId('revealed-event-count')).toContainText(/2 \/ 3|2 \/ 4|2 \/ 5/)
  await expect(page.getByTestId('progressive-worldline').locator('li').nth(1)).toBeVisible()
  await expect(page.getByTestId('process-trace-panel')).toBeVisible()
  await page.locator('.surface-chip').nth(3).click()
  await expect(page.getByTestId('ripple-console')).toBeVisible()

  await page.getByTestId('worldline-next').click()
  await expect(page.getByTestId('progressive-worldline').locator('li').nth(2)).toBeVisible()

  await page.getByTestId('worldline-next').click()
  await expect(page.getByTestId('archive-section')).toBeVisible()
  await expect(page.getByTestId('archive-terminal')).toBeVisible()
  await expect(page.getByTestId('archive-capsule')).toBeVisible()
})

test('viewer can generate a prompt worldline and drive it forward', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByTestId('fixture-grid')).toBeVisible()

  await page.getByTestId('seed-prompt').fill(
    'A bridge load rule changes overnight; tide, steel, and commuter paths begin pulling on each other.',
  )
  await page.getByTestId('prompt-launch').click()

  await expect(page.getByTestId('worldline-theatre')).toBeVisible()
  await expect(page.getByTestId('revealed-event-count')).toContainText(/1 \/ 3|1 \/ 4|1 \/ 5/)
  await expect(page.getByTestId('worldline-theatre')).toContainText(/bridge/i)
  await expect(page.getByTestId('process-trace-panel')).toBeVisible()
  await expect(page.getByTestId('process-file-path')).toContainText(/data\/runtime\/process/)

  await page.getByTestId('worldline-next').click()
  await expect(page.getByTestId('progressive-worldline').locator('li').nth(1)).toBeVisible()
  await expect(page.getByTestId('process-trace-panel')).toContainText(/load|rule|changes/i)
})
