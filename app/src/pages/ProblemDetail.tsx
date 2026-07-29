import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import type { Problem, RunRecord, TestResult } from '../types'
import CodeEditor from '../components/CodeEditor'
import Description from '../components/Description'
import TestResults from '../components/TestResults'
import ThemeToggle from '../components/ThemeToggle'
import History from '../components/History'
import { runTests, warmUpPyodide } from '../pyodide'
import { api } from '../api'
import { timeAgo } from '../time'

type Tab = 'impl' | 'solution' | 'test' | 'history'

export default function ProblemDetail({ problems }: { problems: Problem[] }) {
  const { slug } = useParams()
  const problem = useMemo(
    () => problems.find((p) => p.slug === slug),
    [problems, slug],
  )

  const [tab, setTab] = useState<Tab>('impl')
  const [code, setCode] = useState('')
  const [results, setResults] = useState<TestResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [running, setRunning] = useState(false)
  const [runs, setRuns] = useState<RunRecord[]>([])
  const [lastAllPassedAt, setLastAllPassedAt] = useState<string | null>(null)
  const saveTimer = useRef<number | undefined>(undefined)

  useEffect(() => {
    warmUpPyodide()
  }, [])

  // Load the saved implementation (falling back to the starter) and run history
  // whenever the problem changes.
  useEffect(() => {
    if (!slug || !problem) return
    let cancelled = false
    setResults(null)
    setError(null)
    setTab('impl')
    api
      .getProblem(slug)
      .then((state) => {
        if (cancelled) return
        setCode(state.code ?? problem.starter)
        setLastAllPassedAt(state.lastAllPassedAt)
      })
      .catch(() => {
        if (!cancelled) setCode(problem.starter)
      })
    api
      .listRuns(slug)
      .then((r) => {
        if (!cancelled) setRuns(r)
      })
      .catch(() => {})
    return () => {
      cancelled = true
      clearTimeout(saveTimer.current)
    }
  }, [slug, problem])

  if (!problem) {
    return (
      <div className="page">
        <Link to="/" className="back">
          ← Problems
        </Link>
        <p>Problem not found.</p>
      </div>
    )
  }

  // Debounced autosave — only fires on user edits.
  function scheduleSave(next: string) {
    clearTimeout(saveTimer.current)
    saveTimer.current = window.setTimeout(() => {
      api.saveCode(slug!, next).catch(() => {})
    }, 700)
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
      await api.saveCode(slug!, code).catch(() => {})
      await api.createRun(slug!, { code, passed, failed, total: res.length, durationMs })
      const [freshRuns, state] = await Promise.all([
        api.listRuns(slug!),
        api.getProblem(slug!),
      ])
      setRuns(freshRuns)
      setLastAllPassedAt(state.lastAllPassedAt)
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
        {lastAllPassedAt && (
          <span className="solved on" title="Most recent time all tests passed">
            ✓ solved {timeAgo(lastAllPassedAt)}
          </span>
        )}
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
            <button
              className={tab === 'impl' ? 'active' : ''}
              onClick={() => setTab('impl')}
            >
              Impl
            </button>
            <button
              className={tab === 'solution' ? 'active' : ''}
              onClick={() => setTab('solution')}
            >
              Solution
            </button>
            <button
              className={tab === 'test' ? 'active' : ''}
              onClick={() => setTab('test')}
            >
              Test
            </button>
            <button
              className={tab === 'history' ? 'active' : ''}
              onClick={() => setTab('history')}
            >
              History{runs.length ? ` (${runs.length})` : ''}
            </button>
          </nav>

          {tab === 'impl' && (
            <>
              <CodeEditor value={code} onChange={onCodeChange} />
              <div className="actions">
                <button className="run" onClick={run} disabled={running}>
                  {running ? 'Running…' : 'Run Tests'}
                </button>
                <button className="reset" onClick={() => loadCode(problem.starter)}>
                  Reset
                </button>
              </div>
              {error && <pre className="run-error">{error}</pre>}
              {results && <TestResults results={results} />}
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
