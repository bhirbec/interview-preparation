export type TestStatus = 'pass' | 'fail' | 'error'

export interface TestResult {
  name: string
  status: TestStatus
  message: string
}

export interface RunRecord {
  id: number
  problemId: string
  passed: number
  failed: number
  total: number
  durationMs: number
  allPassed: boolean
  createdAt: string
  code: string
}

export type ProblemStatus = 'not-started' | 'started' | 'solved'

// --- curriculum / lessons ---

export interface LessonSummary {
  id: string
  title: string
  topic: string
  position: number
  exerciseCount: number
  solvedCount: number
  done: boolean
}

export interface LessonsResponse {
  lessons: LessonSummary[]
}

export interface LessonExercise {
  id: string
  title: string
  difficulty: string
  status: ProblemStatus
}

export interface LessonDetail {
  id: string
  title: string
  topic: string
  body: string
  exercises: LessonExercise[]
}

// Status + timing from the latest attempt (returned by both list and detail).
export interface AttemptState {
  status: ProblemStatus
  startedAt: string | null
  accumulatedMs: number
  runningSince: string | null // ISO while the timer runs; null while paused/solved
  solvedAt: string | null
  elapsedMs: number | null // final solve time (ms)
  attemptRunCount: number // Run-Tests clicks in the latest attempt
}

// Row in the paginated catalog list.
export interface ProblemListItem extends AttemptState {
  id: string
  title: string
  difficulty: string
  tags: string[]
}

export interface ProblemPage {
  items: ProblemListItem[]
  total: number
  page: number
  pageSize: number
}

export interface Facet {
  value: string
  count: number
}

export interface Facets {
  difficulties: Facet[]
  tags: Facet[]
}

export type StatusFilter = 'all' | ProblemStatus

// Full problem definition + this user's saved code + latest-attempt state.
export interface ProblemFull extends AttemptState {
  id: string
  title: string
  difficulty: string
  tags: string[]
  sources: string[]
  description: string
  starter: string
  solution: string
  tests: string
  code: string | null
}
