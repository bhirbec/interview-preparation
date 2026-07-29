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
