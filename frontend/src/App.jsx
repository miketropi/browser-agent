import { useState, useEffect } from 'react'
import './App.css'
import MessageBox from './components/MessageBox'
import DashboardTab from './components/DashboardTab'
import { LayoutDashboard, Settings, NotebookText } from 'lucide-react';
import Welcome from './components/Welcome'; 
import TaskBoard from './components/TaskBoard';
function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState('Waiting for backend...')
  const [backendStatus, setBackendStatus] = useState('Checking...')
  const [agentResult, setAgentResult] = useState('')

  useEffect(() => {
    const initializeBackend = async () => {
      try {
        console.log('Waiting for pywebview to be ready...')
        
        // Wait for pywebview to be ready
        await new Promise((resolve) => {
          window.addEventListener('pywebviewready', () => {
            console.log('pywebview is ready!')
            resolve() 
          })
        })

        console.log('Checking for pywebview...', window.pywebview)
        
        // Check if we're running in WebView
        if (window.pywebview && window.pywebview.api) {
          console.log('pywebview detected, initializing...')
          
          // Initialize the API
          await window.pywebview.api.init()
          
          // Call the backend methods
          const result = await window.pywebview.api.get_message()
          console.log('Backend message:', result)
          setMessage(result)
          
          const health = await window.pywebview.api.health_check()
          console.log('Backend health:', health)
          setBackendStatus(health.status)
        } else {
          console.log('pywebview not detected')
          setMessage('Not running in WebView - Make sure to run through Python backend')
          setBackendStatus('WebView not detected')
        }
      } catch (error) {
        console.error('Backend connection error:', error)
        setMessage('Error connecting to backend: ' + error.message)
        setBackendStatus('Error')
      }
    }

    initializeBackend()
  }, [])

  const browserAgent = async (message) => {
    // const message = `
    // 1. Go to https://www.google.com
    // 2. Search for "Current price of Bitcoin"
    // 3. Click on the first result
    // 4. Get current price of Bitcoin and return it as a string formatted as "Current price of Bitcoin: $10000"
    // `
    const result = await window.pywebview.api.run_browser_agent(message)
    console.log('Browser agent result:', result) 
    setAgentResult(result)
  }

  const handleSend = (message) => {
    console.log('Sending message:', message)
    browserAgent(message)
  }

  const tabs = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: <LayoutDashboard size={20} />,
      content: <div>
        <h2>Hi, </h2>
        {/* <Welcome /> */}
      </div>
    },
    {
      id: 'tasks',
      label: 'Tasks',
      icon: <NotebookText size={20} />,
      content: <TaskBoard />
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: <Settings size={20} />,
      content: <div>Settings</div>
    }
  ]

  const handleTabChange = (tabId) => {
    console.log('Tab changed to:', tabId)
  }

  return (
    <div className="font-sans flex flex-col items-center justify-center h-screen bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
      {/* <h1>Browser Agent { backendStatus }</h1> */}
      {/* <button onClick={browserAgent}>Run Browser Agent</button> 
      <p>{ message }</p> */}
      {/* <MessageBox onSend={handleSend} />
      {
        agentResult && (
          <div className="mt-4 p-4 bg-gray-100 rounded-lg shadow-md">
            <p>{ agentResult }</p>
          </div>
        )
      } */}

      <DashboardTab tabs={tabs} defaultActiveTab="dashboard" onTabChange={handleTabChange} />
    </div>
  )
}

export default App
