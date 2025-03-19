import { useState, useEffect } from 'react';
import TaskList from './TaskList';

const initialTasks = [
  {
    id: 1,
    target_website: 'https://www.fleetcard.com.au',
    google_search_keyword: 'compare fuel cards',
    status: 'pending', // pending, doing, completed, failed
    loop: 1,
  },
  {
    id: 2,
    target_website: 'https://www.fleetcard.com.au',
    google_search_keyword: 'fuel card',
    status: 'pending', // pending, doing, completed, failed
    loop: 1,
  }
];

export default function TaskBoard() {
  const [tasks, setTasks] = useState(initialTasks);

  const handleTaskUpdate = (updatedTasks) => {
    setTasks(updatedTasks);
  };

  return (
    <div>
      <h1 className="text-xl font-bold mb-6">Task Board</h1>
      <TaskList tasksData={tasks} onTaskUpdate={handleTaskUpdate} />
    </div>
  )
}