import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import type { TestResult } from '../types'
import CodeEditor from '../components/CodeEditor'
import Description from '../components/Description'
import TestResults from '../components/TestResults'
import AppMenu from '../components/AppMenu'
import History from '../components/History'
import AttemptTimer from '../components/AttemptTimer'
import { runTests, warmUpPyodide } from '../pyodide'
import { api } from '../api'
import { useProblem } from '../hooks/useProblem'
import { useDebouncedSave, SAVE_LABELS } from '../hooks/useDebouncedSave'

type Tab = 'impl' | 'solution' | 'test' | 'history'

export default function ProblemDetail() {
  const id = useParams()['*'] || ''

  const [code, setCode] = useState('')
  const [tab, setTab] = useState<Tab>('impl')
  const [results, setResults] = useState<TestResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [running, setRunning] = useState(false)

  const { problem, setState, notFound, runs, setRuns, reload } = useProblem(
    id,
    (p) => setCode(p.code ?? p.starter),
  )
  const { saveState, scheduleSave, saveNow } = useDebouncedSave(id, code)

  useEffect(() => {
    warmUpPyodide()
  }, [])

  // Reset the transient workspace state when switching problems.
  useEffect(() => {
    setResults(null)
    setError(null)
    setTab('impl')
  }, [id])

  if (notFound) {
    return (
      <div className="page">
        <Link to="/" className="back">
          ← Problems
        </Link>
        <p>Problem not found.</p>
      </div>
    )
  }

  if (!problem) {
    return <div className="loading">Loading…</div>
  }

  function onCodeChange(next: string) {
    setCode(next)
    scheduleSave(next)
  }

  function loadCode(next: string) {
    setCode(next)
    scheduleSave(next)
    setTab('impl')
  }

  async function run() {
    setRunning(true)
    setError(null)
    setResults(null)
    try {
      const { results: res, durationMs } = await runTests(code, problem!.tests)
      setResults(res)
      const passed = res.filter((r) => r.status === 'pass').length
      const failed = res.length - passed
      await saveNow()
      await api.createRun(id, { code, passed, failed, total: res.length, durationMs })
      const [freshRuns, state] = await Promise.all([
        api.listRuns(id),
        api.getProblemState(id),
      ])
      setRuns(freshRuns)
      setState(state)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="page detail">
      <header className="app-header">
        <AppMenu />
        <Link to="/" className="back">
          ← Problems
        </Link>
        <h1>{problem.title}</h1>
        <span className={`badge badge-${problem.difficulty}`}>
          {problem.difficulty}
        </span>
        <AttemptTimer
          id={id}
          attempt={problem}
          onChange={reload}
          onStart={() => loadCode(problem.starter)}
        />
      </header>

      <div className="columns">
        <section className="description">
          <Description text={problem.description} hint={problem.hint} />
          <div className="tags">
            {problem.tags.map((t) => (
              <span key={t} className="tag">
                #{t}
              </span>
            ))}
          </div>
          {problem.sources.length > 0 && (
            <div className="sources">
              {problem.sources.map((s) => (
                <a key={s} href={s} target="_blank" rel="noreferrer">
                  source ↗
                </a>
              ))}
            </div>
          )}
        </section>

        <section className="workspace">
          <nav className="tabs">
            <button className={tab === 'impl' ? 'active' : ''} onClick={() => setTab('impl')}>
              Impl
            </button>
            <button className={tab === 'solution' ? 'active' : ''} onClick={() => setTab('solution')}>
              Solution
            </button>
            <button className={tab === 'test' ? 'active' : ''} onClick={() => setTab('test')}>
              Test
            </button>
            <button className={tab === 'history' ? 'active' : ''} onClick={() => setTab('history')}>
              History{runs.length ? ` (${runs.length})` : ''}
            </button>
          </nav>

          {tab === 'impl' && (
            <>
              <CodeEditor value={code} onChange={onCodeChange} />
              <div className="actions">
                <button
                  className="run"
                  onClick={run}
                  disabled={running || problem.status !== 'started'}
                  title={problem.status !== 'started' ? 'Press Start to begin' : ''}
                >
                  {running ? 'Running…' : 'Run Tests'}
                </button>
                <button className="reset" onClick={() => loadCode(problem.starter)}>
                  Reset
                </button>
                {problem.status !== 'started' && (
                  <span className="run-hint">Press Start to begin</span>
                )}
                <span className={`save-status ${saveState}`} title="Cmd/Ctrl+S to save now">
                  {SAVE_LABELS[saveState]}
                </span>
              </div>
              {error && <pre className="run-error">{error}</pre>}
              {results && (
                <TestResults results={results} onClose={() => setResults(null)} />
              )}
            </>
          )}

          {tab === 'solution' && <CodeEditor value={problem.solution} readOnly />}
          {tab === 'test' && <CodeEditor value={problem.tests} readOnly />}
          {tab === 'history' && (
            <div className="history-wrap">
              <History runs={runs} onLoad={loadCode} />
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
