import { expect, type Page, test } from '@playwright/test'

const EXHIBITION_BUDGET = {
  desktopMinFps: 45,
  nextLatencyMs: 150,
  frameSampleMs: 1200,
  horizontalOverflowPx: 8,
} as const

async function openFixtureWorldline(page: Page) {
  await page.goto('/')
  await expect(page.getByTestId('fixture-grid')).toBeVisible()
  await page.locator('.fixture-card').first().click()
  await page.locator('.primary-action').click()
  await expect(page.getByTestId('worldline-theatre')).toBeVisible()
}

async function sampleFrameCadence(page: Page) {
  return page.evaluate(async (sampleMs) => {
    return new Promise<{ frames: number; duration: number; fps: number; longestFrameMs: number }>((resolve) => {
      let frames = 0
      let previous = performance.now()
      let longestFrameMs = 0
      const startedAt = previous

      function sample(now: number) {
        frames += 1
        longestFrameMs = Math.max(longestFrameMs, now - previous)
        previous = now

        if (now - startedAt >= sampleMs) {
          const duration = Math.max(1, now - startedAt)
          resolve({
            frames,
            duration,
            fps: frames * 1000 / duration,
            longestFrameMs,
          })
          return
        }
        requestAnimationFrame(sample)
      }

      requestAnimationFrame(sample)
    })
  }, EXHIBITION_BUDGET.frameSampleMs)
}

async function sampleNextLatency(page: Page) {
  return page.evaluate(async () => {
    const nextButton = document.querySelector<HTMLButtonElement>('[data-testid="worldline-next"]')
    const counter = document.querySelector('[data-testid="revealed-event-count"]')
    if (!nextButton || !counter) return { latencyMs: 1000, before: '', after: '' }

    const before = counter.textContent ?? ''
    const startedAt = performance.now()

    await new Promise<void>((resolve) => {
      let settled = false
      const observer = new MutationObserver(() => {
        if ((counter.textContent ?? '') !== before) finish()
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
        if ((counter.textContent ?? '') !== before) finish()
      })
      window.setTimeout(finish, 1000)
    })

    return {
      latencyMs: performance.now() - startedAt,
      before,
      after: counter.textContent ?? '',
    }
  })
}

test('canvas frame cadence and next-step latency stay within the local exhibition budget', async ({ page }, testInfo) => {
  await openFixtureWorldline(page)
  await expect(page.getByTestId('process-trace-panel')).toBeVisible()

  const frameSample = await sampleFrameCadence(page)
  const nextSample = await sampleNextLatency(page)

  await testInfo.attach('exhibition-performance.json', {
    body: JSON.stringify({ budget: EXHIBITION_BUDGET, frameSample, nextSample }, null, 2),
    contentType: 'application/json',
  })

  expect(frameSample.fps).toBeGreaterThanOrEqual(EXHIBITION_BUDGET.desktopMinFps)
  expect(nextSample.latencyMs).toBeLessThan(EXHIBITION_BUDGET.nextLatencyMs)
  expect(nextSample.after).not.toBe(nextSample.before)
})

for (const viewport of [
  { name: 'mobile', width: 390, height: 720 },
  { name: 'low-height exhibition', width: 1366, height: 620 },
]) {
  test(`${viewport.name} viewport keeps theatre controls reachable`, async ({ page }) => {
    await page.setViewportSize({ width: viewport.width, height: viewport.height })
    await openFixtureWorldline(page)

    await expect(page.getByTestId('worldline-theatre')).toBeVisible()
    await expect(page.getByTestId('process-trace-panel')).toBeVisible()
    await expect(page.getByTestId('stage-orbit-map')).toBeVisible()
    await page.getByTestId('worldline-next').scrollIntoViewIfNeeded()
    await expect(page.getByTestId('worldline-next')).toBeVisible()

    const viewportHealth = await page.evaluate(() => {
      const nextButton = document.querySelector<HTMLElement>('[data-testid="worldline-next"]')
      const theatre = document.querySelector<HTMLElement>('[data-testid="worldline-theatre"]')
      const process = document.querySelector<HTMLElement>('[data-testid="process-trace-panel"]')
      const nextRect = nextButton?.getBoundingClientRect()
      const theatreRect = theatre?.getBoundingClientRect()
      const processRect = process?.getBoundingClientRect()
      return {
        horizontalOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        nextWithinWidth: !!nextRect && nextRect.left >= -1 && nextRect.right <= window.innerWidth + 1,
        theatreHasHeight: !!theatreRect && theatreRect.height > 280,
        processHasHeight: !!processRect && processRect.height > 80,
      }
    })

    expect(viewportHealth.horizontalOverflow).toBeLessThanOrEqual(EXHIBITION_BUDGET.horizontalOverflowPx)
    expect(viewportHealth.nextWithinWidth).toBe(true)
    expect(viewportHealth.theatreHasHeight).toBe(true)
    expect(viewportHealth.processHasHeight).toBe(true)
  })
}
