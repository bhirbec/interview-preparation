import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'

interface Props {
  value: string
  onChange?: (value: string) => void
  readOnly?: boolean
}

export default function CodeEditor({ value, onChange, readOnly }: Props) {
  return (
    <div className="editor">
      <CodeMirror
        value={value}
        height="380px"
        extensions={[python()]}
        editable={!readOnly}
        readOnly={readOnly}
        onChange={onChange}
        basicSetup={{ tabSize: 2, highlightActiveLine: !readOnly }}
      />
    </div>
  )
}
