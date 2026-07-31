import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { ChapterDetail, ProblemStatus } from '../types'
import AppMenu from '../components/AppMenu'
import { api } from '../api'

const STATUS_ICON: Record<ProblemStatus, string> = {
  solved: '✓',
  started: '◐',
  'not-started': '○',
}
const STATUS_CLASS: Record<ProblemStatus, string> = {
  solved: 'solved',
  started: 'started',
  'not-started': 'none',
}

export default function Chapter() {
  const id = useParams()['*'] || ''
  const [data, setData] = useState<ChapterDetail | null>(null)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    if (!id) return
    let cancelled = false
    setData(null)
    setNotFound(false)
    api
      .getChapter(id)
      .then((c) => !cancelled && setData(c))
      .catch(() => !cancelled && setNotFound(true))
    return () => {
      cancelled = true
    }
  }, [id])

  if (notFound) {
    return (
      <div className="page">
        <header className="app-header">
          <AppMenu />
          <Link to="/program" className="back">
            ← Program
          </Link>
        </header>
        <p>Chapter not found.</p>
      </div>
    )
  }

  if (!data) return <div className="loading">Loading…</div>

  return (
    <div className="page chapter-page">
      <header className="app-header">
        <AppMenu />
        <Link to="/program" className="back">
          ← Program
        </Link>
        <h1>{data.title}</h1>
      </header>

      <div className="chapter-body">
        <article className="lesson">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{data.lesson}</ReactMarkdown>
        </article>

        <section className="chapter-exercises">
          <h3>Exercises</h3>
          <ul className="exercise-list">
            {data.exercises.map((e) => (
              <li key={e.id}>
                <Link to={`/problem/${e.id}`} className="exercise-row">
                  <span className={`status-badge ${STATUS_CLASS[e.status]}`}>
                    {STATUS_ICON[e.status]}
                  </span>
                  <span className="exercise-title">{e.title}</span>
                  <span className={`badge badge-${e.difficulty}`}>{e.difficulty}</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  )
}
