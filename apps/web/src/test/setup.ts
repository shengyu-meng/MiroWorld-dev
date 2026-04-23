Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => undefined,
    removeListener: () => undefined,
    addEventListener: () => undefined,
    removeEventListener: () => undefined,
    dispatchEvent: () => false,
  }),
})

class ResizeObserverStub {
  observe() {}
  disconnect() {}
}

// @ts-expect-error test shim
global.ResizeObserver = ResizeObserverStub

HTMLCanvasElement.prototype.getContext = (() => ({
  clearRect: () => undefined,
  setTransform: () => undefined,
  fillRect: () => undefined,
  beginPath: () => undefined,
  moveTo: () => undefined,
  lineTo: () => undefined,
  bezierCurveTo: () => undefined,
  stroke: () => undefined,
  arc: () => undefined,
  fill: () => undefined,
  createRadialGradient: () => ({
    addColorStop: () => undefined,
  }),
})) as typeof HTMLCanvasElement.prototype.getContext
