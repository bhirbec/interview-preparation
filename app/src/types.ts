export interface Problem {
  slug: string
  title: string
  difficulty: string
  tags: string[]
  sources: string[]
  description: string
  primaryFunction: string
  starter: string
  solution: string
  tests: string
}

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

export interface ProblemState {
  code: string | null
  updatedAt: string | null
  runCount: number
  lastAllPassedAt: string | null
}

export type SummaryMap = Record<
  string,
  { runCount: number; lastAllPassedAt: string | null }
>
