import React from 'react'

const Header = ({ showInstallButton, onInstallClick }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-br from-blue-500 to-purple-600 p-2 rounded-xl">
            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
              <span className="text-blue-600 font-bold text-xl">E</span>
            </div>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-800">EduBot</h1>
            <p className="text-sm text-gray-600">Tu Asistente de Estudio</p>
          </div>
        </div>

        {showInstallButton && (
          <button
            onClick={onInstallClick}
            className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:opacity-90 transition-opacity flex items-center space-x-2 shadow-md"
            aria-label="Instalar aplicación"
          >
            <span>Agregar a inicio</span>
          </button>
        )}
      </div>
    </header>
  )
}

export default Header
