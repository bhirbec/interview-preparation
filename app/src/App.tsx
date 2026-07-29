import { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import type { Problem } from './types'
import ProblemList from './pages/ProblemList'
import ProblemDetail from './pages/ProblemDetail'

export default function App() {
  const [problems, setProblems] = useState<Problem[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}problems.json`)
      .then((r) => {
        if (!r.ok) throw new Error(`Failed to load problems.json (${r.status})`)
        return r.json()
      })
      .then(setProblems)
      .catch((e) => setError(String(e?.message ?? e)))
  }, [])

  if (error) return <div className="loading">Error: {error}</div>
  if (!problems) return <div className="loading">Loading problems…</div>

  return (
    <Routes>
      <Route path="/" element={<ProblemList problems={problems} />} />
      <Route path="/problem/:slug" element={<ProblemDetail problems={problems} />} />
    </Routes>
  )
}
