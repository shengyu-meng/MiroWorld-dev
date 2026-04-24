import { expect, type Page, test } from '@playwright/test'

async function openFixtureWorldline(page: Page) {
  await page.goto('/')
  await expect(page.getByTestId('fixture-grid')).toBeVisible()
  await page.locator('.fixture-card').first().click()
  await page.locator('.primary-action').click()
  await expect(page.getByTestId('worldline-theatre')).toBeVisible()
}

test('canvas frame cadence and next-step latency stay within the local exhibition budget', async ({ page }) => {
  await openFixtureWorldline(page)
  await expect(page.getByTestId('process-trace-panel')).toBeVisible()

  const frameSample = await page.evaluate(async () => {
    return new Promise<{ frames: number; duration: number; fps: number }>((resolve) => {
      let frames = 0
      const startedAt = performance.now()

      function sample(now: number) {
        frames += 1
        if (now - startedAt >= 900) {
          const duration = Math.max(1, now - startedAt)
          resolve({
            frames,
            duration,
            fps: frames * 1000 / duration,
          })
          return
        }
        requestAnimationFrame(sample)
      }

      requestAnimationFrame(sample)
    })
  })

  expect(frameSample.fps).toBeGreaterThan(24)

  const nextLatency = await page.evaluate(async () => {
    const nextButton = document.querySelector<HTMLButtonElement>('[data-testid="worldline-next"]')
    const counter = document.querySelector('[data-testid="revealed-event-count"]')
    if (!nextButton || !counter) return 1000

    const before = counter.textContent
    const startedAt = performance.now()

    await new Promise<void>((resolve) => {
      let settled = false
      const observer = new MutationObserver(() => {
        if (counter.textContent !== before) finish()
      })

      function finish() {
        if (settled) return
        settled = true
        observer.disconnect()
        resolve()
      }

      observer.observe(counter, { childList: true, subtree: true, characterData: true })
      nextButton.click()
      requestAnimationFrame(() => {
        if (counter.textContent !== before) finish()
      })
      window.setTimeout(finish, 1000)
    })

    return performance.now() - startedAt
  })

  expect(nextLatency).toBeLessThan(300)
})
