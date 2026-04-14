function ThemeBanner({ theme, date }) {
  return (
    <header className="banner-theme">
      <h1 className="title">MINDFORGE</h1>
      <p className="theme">
        Today's theme: <strong>{theme.toUpperCase()}</strong>
      </p>
      <p className="date">{date}</p>
    </header>
  )
}

export default ThemeBanner
