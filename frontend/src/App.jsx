import { useState, useEffect } from 'react'
import './App.css'
import MessageBox from './components/MessageBox'
import DashboardTab from './components/DashboardTab'
import { LayoutDashboard, Settings, NotebookText } from 'lucide-react';
import Welcome from './components/Welcome'; 
import TaskBoard from './components/TaskBoard';
import SettingsTab from './components/SettingsTab';

import useStore from './libs/store'

function App() {
  const { tasks, setTasks, settings, setSettings } = useStore()

  const getTasks = async () => {
    const { tasks } = await window.pywebview.api.get_tasks()
    setTasks(tasks)
  }

  const getSettings = async () => {
    const { settings } = await window.pywebview.api.get_settings()
    setSettings(settings)
  }

  useEffect(() => {
    const initializeBackend = async () => {
      window.addEventListener('pywebviewready', async () => {
        console.log('pywebview is ready!')
        await window.pywebview.api.init()

        const health = await window.pywebview.api.health_check()
        console.log('Backend health:', health)

        getTasks();
        getSettings();
      })

      
    }

    initializeBackend()
  }, [])

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
      content: <SettingsTab />
    }
  ]

  const handleTabChange = (tabId) => {
    console.log('Tab changed to:', tabId)
  }

  return (
    <div className="font-sans flex flex-col items-center justify-center h-screen bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">      
      {/* { JSON.stringify(settings) } */}
      <DashboardTab tabs={tabs} defaultActiveTab="dashboard" onTabChange={handleTabChange} />
    </div>
  )
}

export default App
