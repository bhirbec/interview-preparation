import { useEffect, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import type { ProblemFull, RunRecord, TestResult } from '../types'
import CodeEditor from '../components/CodeEditor'
import Description from '../components/Description'
import TestResults from '../components/TestResults'
import ThemeToggle from '../components/ThemeToggle'
import History from '../components/History'
import AttemptTimer from '../components/AttemptTimer'
import { runTests, warmUpPyodide } from '../pyodide'
import { api } from '../api'

type Tab = 'impl' | 'solution' | 'test' | 'history'
type SaveState = 'idle' | 'unsaved' | 'saving' | 'saved' | 'error'

const SAVE_LABELS: Record<SaveState, string> = {
  idle: '',
  unsaved: '● Unsaved',
  saving: 'Saving…',
  saved: 'Saved ✓',
  error: 'Save failed',
}

export default function ProblemDetail() {
  const id = useParams()['*'] || ''

  const [problem, setProblem] = useState<ProblemFull | null>(null)
  const [notFound, setNotFound] = useState(false)
  const [tab, setTab] = useState<Tab>('impl')
  const [code, setCode] = useState('')
  const [results, setResults] = useState<TestResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [running, setRunning] = useState(false)
  const [runs, setRuns] = useState<RunRecord[]>([])
  const [saveState, setSaveState] = useState<SaveState>('idle')
  const saveTimer = useRef<number | undefined>(undefined)
  const codeRef = useRef(code)
  codeRef.current = code
  const saveNowRef = useRef<() => void>(() => {})

  useEffect(() => {
    warmUpPyodide()
  }, [])

  // Cmd/Ctrl+S saves immediately (and suppresses the browser's Save dialog).
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 's') {
        e.preventDefault()
        saveNowRef.current()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  // Load the full problem (definition + saved code + runs) on id change.
  useEffect(() => {
    if (!id) return
    let cancelled = false
    setProblem(null)
    setNotFound(false)
    setResults(null)
    setError(null)
    setSaveState('idle')
    setTab('impl')
    api
      .getProblem(id)
      .then((p) => {
        if (cancelled) return
        if (!p || !('id' in p)) {
          setNotFound(true)
          return
        }
        setProblem(p)
        setCode(p.code ?? p.starter)
      })
      .catch(() => !cancelled && setNotFound(true))
    api
      .listRuns(id)
      .then((r) => !cancelled && setRuns(r))
      .catch(() => {})
    return () => {
      cancelled = true
      clearTimeout(saveTimer.current)
    }
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

  // Refetch problem (attempt status/timing) after a timer action or a run.
  function reload() {
    api.getProblem(id).then((p) => {
      if (p && 'id' in p) setProblem(p)
    })
  }

  function doSave(next: string) {
    setSaveState('saving')
    return api
      .saveCode(id, next)
      .then(() => setSaveState('saved'))
      .catch(() => setSaveState('error'))
  }

  function scheduleSave(next: string) {
    setSaveState('unsaved')
    clearTimeout(saveTimer.current)
    saveTimer.current = window.setTimeout(() => doSave(next), 700)
  }

  saveNowRef.current = () => {
    clearTimeout(saveTimer.current)
    doSave(codeRef.current)
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
      clearTimeout(saveTimer.current)
      await doSave(code)
      await api.createRun(id, { code, passed, failed, total: res.length, durationMs })
      const [freshRuns, state] = await Promise.all([api.listRuns(id), api.getProblem(id)])
      setRuns(freshRuns)
      if (state && 'id' in state) setProblem(state)
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="page detail">
      <header className="app-header">
        <Link to="/" className="back">
          ← Problems
        </Link>
        <h1>{problem.title}</h1>
        <span className={`badge badge-${problem.difficulty}`}>
          {problem.difficulty}
        </span>
        <AttemptTimer id={id} attempt={problem} onChange={reload} />
        <ThemeToggle />
      </header>

      <div className="columns">
        <section className="description">
          <Description text={problem.description} />
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
