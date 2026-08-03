// Curriculum view models, ported from server.lessons and server.get_lesson.
// Pure: no React, no fetching.
//
// Two asymmetries in the original are deliberate and preserved:
//
//   1. exerciseCount counts the RAW exercise ids, including ones missing from
//      the catalog (the list endpoint did a plain len()), while the detail view
//      drops them from the displayed list.
//   2. "Solved" means EVER solved, not "the latest attempt is solved". After a
//      Retake the latest attempt is unsolved, but the lesson must stay complete.
//      On the lesson page ever-solved also outranks "latest attempt started", so
//      a retaken problem reads `solved` here and `started` in the catalog list.
import type {
  CatalogProblem,
  LessonContent,
  LessonDetail,
  LessonSummary,
  ProblemStatus,
} from './types'
import { everSolved, statusOf, type Progress } from './progress'

export function lessonSummaries(
  lessons: LessonContent[],
  progress: Progress,
): LessonSummary[] {
  return lessons.map((l) => {
    const solvedCount = l.exercises.filter((e) => everSolved(progress, e)).length
    return {
      id: l.id,
      title: l.title,
      topic: l.topic,
      position: l.position,
      exerciseCount: l.exercises.length,
      solvedCount,
      done: solvedCount >= 1,
    }
  })
}

function exerciseStatus(progress: Progress, id: string): ProblemStatus {
  if (everSolved(progress, id)) return 'solved'
  return statusOf(progress, id) === 'started' ? 'started' : 'not-started'
}

export function lessonDetail(
  lesson: LessonContent | undefined,
  catalog: CatalogProblem[],
  progress: Progress,
): LessonDetail | null {
  if (!lesson) return null
  const byId = new Map(catalog.map((p) => [p.id, p]))
  const exercises = []
  for (const e of lesson.exercises) {
    const p = byId.get(e)
    if (!p) continue // exercise id no longer in the catalog
    exercises.push({
      id: e,
      title: p.title,
      difficulty: p.difficulty,
      status: exerciseStatus(progress, e),
    })
  }
  return {
    id: lesson.id,
    title: lesson.title,
    topic: lesson.topic,
    body: lesson.body,
    exercises,
  }
}
