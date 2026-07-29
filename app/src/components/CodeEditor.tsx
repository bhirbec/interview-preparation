import CodeMirror, { keymap, Prec } from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { acceptCompletion } from '@codemirror/autocomplete'
import { indentWithTab } from '@codemirror/commands'
import { useTheme } from '../theme'

interface Props {
  value: string
  onChange?: (value: string) => void
  readOnly?: boolean
}

// Tab accepts the active autocompletion; when no completion popup is open it
// falls through to indentation (Shift-Tab dedents).
const tabKeymap = Prec.highest(
  keymap.of([{ key: 'Tab', run: acceptCompletion }, indentWithTab]),
)

export default function CodeEditor({ value, onChange, readOnly }: Props) {
  const { theme } = useTheme()
  return (
    <div className="editor">
      <CodeMirror
        value={value}
        height="100%"
        theme={theme}
        extensions={[python(), tabKeymap]}
        editable={!readOnly}
        readOnly={readOnly}
        onChange={onChange}
        basicSetup={{ tabSize: 2, highlightActiveLine: !readOnly }}
      />
    </div>
  )
}
