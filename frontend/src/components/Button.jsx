import React from 'react'

const Button = ({ buttonClass, text, disabled, onClick }) => {
  return (
    <button className={`button ${buttonClass}`}
      disabled={disabled}
      onClick={onClick}
    >
      {text}
    </button>
  )
}

export default Button
