import type { RunRecord } from '../types'
import { timeAgo, formatDateTime } from '../time'

interface Props {
  runs: RunRecord[]
  onLoad: (code: string) => void
}

export default function History({ runs, onLoad }: Props) {
  if (runs.length === 0) {
    return <div className="history-empty">No runs yet. Run the tests to build history.</div>
  }

  return (
    <ul className="history">
      {runs.map((r) => (
        <li key={r.id} className={`history-row ${r.allPassed ? 'passed' : 'failed'}`}>
          <span className="icon">{r.allPassed ? '✅' : '❌'}</span>
          <span className="score">
            {r.passed}/{r.total}
          </span>
          <span className="dur">{Math.round(r.durationMs)} ms</span>
          <span className="when" title={formatDateTime(r.createdAt)}>
            {timeAgo(r.createdAt)}
          </span>
          <button type="button" className="load" onClick={() => onLoad(r.code)}>
            Load
          </button>
        </li>
      ))}
    </ul>
  )
}
