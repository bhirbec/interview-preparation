import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { LessonDetail, ProblemStatus } from '../types'
import AppMenu from '../components/AppMenu'
import { api } from '../api'
import { loadCatalog, loadLessons } from '../content'
import { lessonDetail } from '../lessons'
import { indexProgress } from '../progress'

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

export default function Lesson() {
  const id = useParams()['*'] || ''
  const [data, setData] = useState<LessonDetail | null>(null)
  const [notFound, setNotFound] = useState(false)

  useEffect(() => {
    if (!id) return
    let cancelled = false
    setData(null)
    setNotFound(false)
    Promise.all([loadLessons(), loadCatalog(), api.getProgress()])
      .then(([lessons, catalog, progress]) => {
        if (cancelled) return
        const detail = lessonDetail(
          lessons.lessons.find((l) => l.id === id),
          catalog.problems,
          indexProgress(progress.problems),
        )
        if (detail) setData(detail)
        else setNotFound(true)
      })
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
        <p>Lesson not found.</p>
      </div>
    )
  }

  if (!data) return <div className="loading">Loading…</div>

  return (
    <div className="page lesson-page">
      <header className="app-header">
        <AppMenu />
        <Link to="/program" className="back">
          ← Program
        </Link>
        <h1>{data.title}</h1>
      </header>

      <div className="lesson-body">
        <article className="lesson">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{data.body}</ReactMarkdown>
        </article>

        <section className="lesson-exercises">
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
