import React from 'react'
import Header from './components/Header'
import Chat from './components/Chat'

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header showInstallButton={false} onInstallClick={() => {}} />
      <main className="flex-1 flex">
        <Chat />
      </main>
    </div>
  )
}

export default App
