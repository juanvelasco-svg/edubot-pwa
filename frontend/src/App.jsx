import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import Chat from './components/Chat'
import { registerSW } from 'virtual:pwa-register'

function App() {
  const [showInstallPrompt, setShowInstallPrompt] = useState(false)
  const [deferredPrompt, setDeferredPrompt] = useState(null)
  const [isStandalone, setIsStandalone] = useState(false)

  useEffect(() => {
    const updateSW = registerSW({
      onNeedRefresh() {
        if (confirm('Nueva versión disponible. ¿Quieres actualizar?')) {
          updateSW(true)
        }
      },
      onOfflineReady() {
        console.log('App lista para funcionar offline')
      }
    })

    const isStandaloneMode = window.matchMedia('(display-mode: standalone)').matches
    setIsStandalone(isStandaloneMode)

    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault()
      setDeferredPrompt(e)
      setShowInstallPrompt(true)
    }

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    }
  }, [])

  const handleInstallClick = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt()
      const { outcome } = await deferredPrompt.userChoice
      
      if (outcome === 'accepted') {
        console.log('Usuario aceptó instalar la app')
      }
      
      setDeferredPrompt(null)
      setShowInstallPrompt(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header 
        showInstallButton={showInstallPrompt && !isStandalone} 
        onInstallClick={handleInstallClick}
      />
      <main className="flex-1 flex">
        <Chat />
      </main>
    </div>
  )
}

export default App
