import type { TestResult } from '../types'

interface Props {
  results: TestResult[]
  onClose: () => void
}

export default function TestResults({ results, onClose }: Props) {
  const passed = results.filter((r) => r.status === 'pass').length
  const allPass = passed === results.length && results.length > 0

  return (
    <div className="results">
      <div className={`summary ${allPass ? 'all-pass' : 'has-fail'}`}>
        <span>
          {passed}/{results.length} passed
        </span>
        <button
          type="button"
          className="results-close"
          onClick={onClose}
          title="Close results"
          aria-label="Close results"
        >
          ✕
        </button>
      </div>
      <ul>
        {results.map((r) => (
          <li key={r.name} className={`result result-${r.status}`}>
            <div className="result-head">
              <span className="icon">{r.status === 'pass' ? '✅' : '❌'}</span>
              <span className="name">{r.name}</span>
              <span className="status">{r.status}</span>
            </div>
            {r.status !== 'pass' && <pre className="msg">{r.message}</pre>}
          </li>
        ))}
      </ul>
    </div>
  )
}
