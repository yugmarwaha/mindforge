function Grid({ rows, currentGuess, maxGuesses, wordLength, shake }) {
  const gridRows = []
  for (let r = 0; r < maxGuesses; r++) {
    const submitted = r < rows.length
    const isCurrent = r === rows.length
    const cells = []
    for (let c = 0; c < wordLength; c++) {
      let letter = ''
      let state = 'empty'
      if (submitted) {
        letter = rows[r].guess[c]
        state = rows[r].feedback[c]
      } else if (isCurrent && c < currentGuess.length) {
        letter = currentGuess[c]
        state = 'filled'
      }
      cells.push(
        <div key={c} className={`cell cell-${state}`}>
          {letter}
        </div>
      )
    }
    const rowClass =
      'grid-row' + (isCurrent && shake ? ' grid-row-shake' : '')
    gridRows.push(
      <div key={r} className={rowClass}>
        {cells}
      </div>
    )
  }
  return <div className="grid">{gridRows}</div>
}

export default Grid
