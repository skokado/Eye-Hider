import React from 'react'

const Header = () => {
  return (
    <nav className="navbar" role="navigation" aria-label="main navigation">
      <div className="navbar-brand">
        <a href="/" className="navbar-item">
          <img src={`${process.env.PUBLIC_URL}/img/logo.png`} alt=""></img>
        </a>
      </div>
    </nav>
  )
}

export default Header
