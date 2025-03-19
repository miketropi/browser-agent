import { useState, useEffect } from 'react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Edit, Trash2, GripVertical, Plus, Play, Loader2 } from 'lucide-react';

const SortableItem = ({ numIndex, task, onEdit, onDelete }) => {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: task.id });
  
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };
  
  const statusColors = {
    pending: 'bg-yellow-100 text-yellow-800',
    doing: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800'
  };

  return (
    <tr 
      ref={setNodeRef} 
      style={style} 
      className={`border-b hover:bg-gray-50 dark:hover:bg-gray-800 ${task.status === 'doing' ? 'bg-blue-50 dark:bg-blue-900/20 animate-pulse' : ''}`}
    >
      <td className="p-2">
        <div {...attributes} {...listeners} className="cursor-move flex justify-center">
          <GripVertical size={18} className="text-gray-400" />
        </div>
      </td>
      <td className="p-3">{ numIndex }</td>
      <td className="p-3 max-w-xs truncate">{task.target_website}</td>
      <td className="p-3">{task.google_search_keyword}</td>
      <td className="p-3">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[task.status]}`}>
          {task.status}
        </span>
      </td>
      <td className="p-3">{task.loop}</td>
      <td className="p-3">
        <div className="flex space-x-2">
          <button onClick={() => onEdit(task)} className="p-1 text-blue-600 hover:text-blue-800">
            <Edit size={18} />
          </button>
          <button onClick={() => onDelete(task.id)} className="p-1 text-red-600 hover:text-red-800">
            <Trash2 size={18} />
          </button>
        </div>
      </td>
    </tr>
  );
};

const TaskForm = ({ task, onSave, onCancel }) => {
  const [formData, setFormData] = useState(task || {
    target_website: '',
    google_search_keyword: '',
    status: 'pending',
    loop: 1
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">{task ? 'Edit Task' : 'Add New Task'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Target Website</label>
            <input
              type="text"
              name="target_website"
              value={formData.target_website}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Google Search Keyword</label>
            <input
              type="text"
              name="google_search_keyword"
              value={formData.google_search_keyword}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
            >
              <option value="pending">Pending</option>
              <option value="doing">Doing</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">Loop</label>
            <input
              type="number"
              name="loop"
              value={formData.loop}
              onChange={handleChange}
              className="w-full p-2 border rounded-md"
              min="1"
              required
            />
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 border rounded-md hover:bg-gray-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default function TaskList({ tasksData, onTaskUpdate }) {
  const [tasks, setTasks] = useState(tasksData);
  const [editingTask, setEditingTask] = useState(null);
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [isRunningTasks, setIsRunningTasks] = useState(false);
  // result of browser agent
  const [browserAgentResult, setBrowserAgentResult] = useState(null);

  useEffect(() => {
    onTaskUpdate(tasks);
  }, [tasks]);
  
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor)
  );

  const handleDragEnd = (event) => {
    const { active, over } = event;
    
    if (active.id !== over.id) {
      setTasks((items) => {
        const oldIndex = items.findIndex(item => item.id === active.id);
        const newIndex = items.findIndex(item => item.id === over.id);
        
        const newItems = [...items];
        const [movedItem] = newItems.splice(oldIndex, 1);
        newItems.splice(newIndex, 0, movedItem);
        
        return newItems;
      });
    }
  };

  const handleEdit = (task) => {
    setEditingTask(task);
  };

  const handleDelete = (id) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setTasks(tasks.filter(task => task.id !== id));
    }
  };

  const handleSave = (taskData) => {
    if (editingTask) {
      // Edit existing task
      setTasks(tasks.map(task => 
        task.id === editingTask.id ? { ...taskData, id: task.id } : task
      ));
      setEditingTask(null);
    } else {
      // Add new task
      const newId = Math.max(0, ...tasks.map(t => t.id)) + 1;
      setTasks([...tasks, { ...taskData, id: newId }]);
      setIsAddingTask(false);
    }
  };

  const browserAgent = async (task) => {
    const result = await window.pywebview.api.task_reception(task)
    return result
  }

  const handleRunTasks = async () => {
    if (tasks.length === 0) {
      alert('No tasks to run. Please add tasks first.');
      return;
    }

    setIsRunningTasks(true)
    
    
    // filter tasks with status pending
    const pendingTasks = tasks.filter(task => task.status === 'pending')

    if (pendingTasks.length === 0) {
      alert('No tasks to run. Please add tasks first.');
      return;
    }

    // loop and handle async for each item doing step by step task item, and wait for all tasks to complete, and then set isRunningTasks to false, only for tasks status is pending
    for (const task of pendingTasks) {
      // update task status to doing
      setTasks(prev => prev.map(t => t.id === task.id ? { ...t, status: 'doing' } : t))

      console.log('___Task status updated to doing:', task)
      const result = await browserAgent(task)
      console.log('___Browser agent result:', result)

      setBrowserAgentResult(result)

      // update task status to completed
      setTasks(prev => prev.map(t => t.id === task.id ? { ...t, status: 'completed' } : t))
    }

    setIsRunningTasks(false)
  };

  return (
    <div className="w-full bg-white dark:bg-gray-900 shadow-md rounded-lg overflow-hidden border">
      <div className="p-4 flex justify-between items-center border-b">
        <h2 className="text-lg font-semibold">Task Manager</h2>
        <div className="flex space-x-2">
          <button 
            onClick={() => setIsAddingTask(true)}
            className="flex items-center px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <Plus size={16} className="mr-1" />
            Add Task
          </button>

          <button 
            onClick={() => {
              if (tasks.length === 0) {
                alert('No tasks to run. Please add tasks first.');
                return;
              }
              if (window.confirm('Are you sure you want to run tasks?')) {
                handleRunTasks()
              }
            }}
            className="flex items-center px-3 py-1.5 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            {isRunningTasks ? (
              <Loader2 size={16} className="mr-1 animate-spin" />
            ) : (
              <Play size={16} className="mr-1" />
            )}
            Run Tasks
          </button>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              <th className="p-3 w-10"></th>
              <th className="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order</th>
              <th className="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Target Website</th>
              <th className="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Search Keyword</th>
              <th className="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Loop</th>
              <th className="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
            <DndContext 
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={handleDragEnd}
            >
              <SortableContext 
                items={tasks.map(task => task.id)}
                strategy={verticalListSortingStrategy}
              >
                {tasks.map((task, index) => (
                  <SortableItem 
                    key={task.id} 
                    task={task} 
                    numIndex={index + 1}
                    onEdit={handleEdit} 
                    onDelete={handleDelete} 
                  />
                ))}
              </SortableContext>
            </DndContext>
          </tbody>
        </table>
      </div>
      
      {tasks.length === 0 && (
        <div className="p-8 text-center text-gray-500">
          No tasks found. Click "Add Task" to create one.
        </div>
      )}
      
      {(editingTask || isAddingTask) && (
        <TaskForm 
          task={editingTask} 
          onSave={handleSave} 
          onCancel={() => {
            setEditingTask(null);
            setIsAddingTask(false);
          }} 
        />
      )}

      {browserAgentResult && (
        <div className="p-4">
          <h2 className="text-lg font-semibold">Browser Agent Result</h2>
          <pre>{JSON.stringify(browserAgentResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

