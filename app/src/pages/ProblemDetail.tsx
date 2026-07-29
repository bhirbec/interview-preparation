import { useEffect, useMemo, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import type { Problem, TestResult } from '../types'
import CodeEditor from '../components/CodeEditor'
import TestResults from '../components/TestResults'
import ThemeToggle from '../components/ThemeToggle'
import { runTests, warmUpPyodide } from '../pyodide'

type Tab = 'impl' | 'solution' | 'test'

export default function ProblemDetail({ problems }: { problems: Problem[] }) {
  const { slug } = useParams()
  const problem = useMemo(
    () => problems.find((p) => p.slug === slug),
    [problems, slug],
  )

  const [tab, setTab] = useState<Tab>('impl')
  const [code, setCode] = useState(problem?.starter ?? '')
  const [results, setResults] = useState<TestResult[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [running, setRunning] = useState(false)

  // Start fetching the Pyodide runtime as soon as a problem is opened.
  useEffect(() => {
    warmUpPyodide()
  }, [])

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

  async function run() {
    setRunning(true)
    setError(null)
    setResults(null)
    try {
      setResults(await runTests(code, problem!.tests))
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
        <ThemeToggle />
      </header>

      <div className="columns">
        <section className="description">
          <pre className="prose">{problem.description}</pre>
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
          </nav>

          {tab === 'impl' && (
            <>
              <CodeEditor value={code} onChange={setCode} />
              <div className="actions">
                <button className="run" onClick={run} disabled={running}>
                  {running ? 'Running…' : 'Run Tests'}
                </button>
                <button className="reset" onClick={() => setCode(problem.starter)}>
                  Reset
                </button>
              </div>
              {error && <pre className="run-error">{error}</pre>}
              {results && <TestResults results={results} />}
            </>
          )}

          {tab === 'solution' && (
            <CodeEditor value={problem.solution} readOnly />
          )}
          {tab === 'test' && <CodeEditor value={problem.tests} readOnly />}
        </section>
      </div>
    </div>
  )
}
