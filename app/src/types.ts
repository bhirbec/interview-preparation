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

// Row in the paginated catalog list.
export interface ProblemListItem {
  id: string
  title: string
  difficulty: string
  tags: string[]
  lastAllPassedAt: string | null
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

export type SolvedFilter = 'all' | 'solved' | 'unsolved'

// Full problem definition + this user's saved code and status.
export interface ProblemFull {
  id: string
  title: string
  difficulty: string
  tags: string[]
  sources: string[]
  description: string
  primaryFunction: string
  starter: string
  solution: string
  tests: string
  code: string | null
  runCount: number
  lastAllPassedAt: string | null
}
