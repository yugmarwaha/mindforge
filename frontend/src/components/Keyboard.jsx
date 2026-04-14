const KEYBOARD_ROWS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
]

function Keyboard({ onLetter, onEnter, onBackspace, letterStates, disabled }) {
  return (
    <div className="keyboard">
      {KEYBOARD_ROWS.map((row, i) => (
        <div key={i} className="kb-row">
          {i === 2 && (
            <button
              type="button"
              className="key key-wide"
              onClick={onEnter}
              disabled={disabled}
            >
              Enter
            </button>
          )}
          {row.map(letter => {
            const state = letterStates[letter] || 'default'
            return (
              <button
                key={letter}
                type="button"
                className={`key key-${state}`}
                onClick={() => onLetter(letter)}
                disabled={disabled}
              >
                {letter}
              </button>
            )
          })}
          {i === 2 && (
            <button
              type="button"
              className="key key-wide"
              onClick={onBackspace}
              disabled={disabled}
            >
              ⌫
            </button>
          )}
        </div>
      ))}
    </div>
  )
}

export default Keyboard
