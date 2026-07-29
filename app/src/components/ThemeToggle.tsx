import { useTheme } from '../theme'

export default function ThemeToggle() {
  const { theme, toggle } = useTheme()
  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={toggle}
      title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
      aria-label="Toggle color theme"
    >
      {theme === 'dark' ? '☀️' : '🌙'}
    </button>
  )
}
