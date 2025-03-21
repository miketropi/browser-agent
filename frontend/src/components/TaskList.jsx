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
    pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-200',
    doing: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-200',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-200',
    failed: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-200'
  };

  return (
    <tr 
      ref={setNodeRef} 
      style={style} 
      className={`border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 ${task.status === 'doing' ? 'bg-blue-50 dark:bg-blue-900/20 animate-pulse' : ''}`}
    >
      <td className="p-2">
        <div {...attributes} {...listeners} className="cursor-move flex justify-center">
          <GripVertical size={18} className="text-gray-400 dark:text-gray-500" />
        </div>
      </td>
      <td className="p-3 dark:text-gray-200">{ numIndex }</td>
      <td className="p-3 max-w-xs truncate dark:text-gray-200">{task.target_website}</td>
      <td className="p-3 dark:text-gray-200">{task.search_keyword}</td>
      <td className="p-3">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[task.status]}`}>
          {task.status}
        </span>
      </td>
      {/* <td className="p-3">{task.loop}</td> */}
      <td className="p-3">
        <div className="flex space-x-2">
          <button onClick={() => onEdit(task)} className="p-1 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
            <Edit size={18} />
          </button>
          <button onClick={() => onDelete(task.id)} className="p-1 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300">
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
    search_keyword: '',
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
        <h2 className="text-xl font-semibold mb-4 dark:text-white">{task ? 'Edit Task' : 'Add New Task'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 dark:text-gray-200">Target Website</label>
            <input
              type="text"
              name="target_website"
              value={formData.target_website}
              onChange={handleChange}
              className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 dark:text-gray-200">Google Search Keyword</label>
            <input
              type="text"
              name="search_keyword"
              value={formData.search_keyword}
              onChange={handleChange}
              className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1 dark:text-gray-200">Status</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="w-full p-2 border rounded-md dark:bg-gray-700 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
            >
              <option value="pending">Pending</option>
              <option value="doing">Doing</option>
              <option value="completed">Completed</option>
              <option value="failed">Failed</option>
            </select>
          </div>
          {/* <div className="mb-4">
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
          </div> */}
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 border rounded-md hover:bg-gray-100 dark:border-gray-600 dark:text-gray-200 dark:hover:bg-gray-700"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
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
  const [browserAgentResults, setBrowserAgentResults] = useState([])

  useEffect(() => {
    onTaskUpdate(tasks);
  }, [tasks]);

  useEffect(() => {
    setTasks(tasksData)
  }, [tasksData])
  
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

  const handleEdit = async (task) => {
    // console.log('___Edit task:', task)

    setEditingTask(task);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this task?')) {

      // delete task with api
      const result = await window.pywebview.api.delete_task(id)
      console.log('___Delete task result:', result)

      if (result.status === 'success') {
        setTasks(tasks.filter(task => task.id !== id));
      } else {
        alert('Failed to delete task. Please try again.')
      }
    }
  };

  // add a function to handle add task with api
  const handleAddTaskDb = async (taskData) => {
    const result = await window.pywebview.api.add_task(taskData)
    return result
  }

  const handleSave = async (taskData) => {
    if (editingTask) {

      // update task with api
      let { date_add, ...rest } = taskData
      const result = await window.pywebview.api.update_task(rest)
      console.log('___Update task result:', result)
      // return;

      if (result.status === 'success') {
        setTasks(tasks.map(task => 
          task.id === editingTask.id ? { ...task, ...taskData, id: task.id } : task
        ));
        setEditingTask(null);
      } else {
        alert('Failed to update task. Please try again.')
      }

    } else {

      // handle add task with api
      console.log('___Add task data:', taskData)
      const result = await handleAddTaskDb(taskData)
      console.log('___Add task result:', result)

      if (result.status === 'success') {
        setTasks([...tasks, result.task])
      } else {
        alert('Failed to add task. Please try again.')
      }

      // Add new task
      // const newId = Math.max(0, ...tasks.map(t => t.id)) + 1;
      // setTasks([...tasks, { ...taskData, id: newId }]);

      setIsAddingTask(false);
    }
  };

  const browserAgent = async (task) => {
    const result = await window.pywebview.api.task_reception(task)
    return result
  }

  // make a function delay 2s
  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  const handleRunTasks = async () => {
    if (tasks.length === 0) {
      alert('No tasks to run. Please add tasks first.');
      return;
    }
    
    // filter tasks with status pending
    const pendingTasks = tasks.filter(task => task.status === 'pending')

    if (pendingTasks.length === 0) {
      alert('No tasks to run. Please add tasks first.');
      return;
    }

    setIsRunningTasks(true)

    // loop and handle async for each item doing step by step task item, and wait for all tasks to complete, and then set isRunningTasks to false, only for tasks status is pending
    for (const task of pendingTasks) {
      // update task status to doing
      setTasks(prev => prev.map(t => t.id === task.id ? { ...t, status: 'doing' } : t))

      console.log('___Task status updated to doing:', task)
      const result = await browserAgent(task)
      await delay(2000)

      console.log('___Browser agent result:', result)

      // set browser agent results
      setBrowserAgentResults(prev => [...prev, {
        taskId: task.id,
        result: result
      }])

      // update task status to completed
      setTasks(prev => prev.map(t => t.id === task.id ? { ...t, status: 'completed' } : t))
    }

    setIsRunningTasks(false)
  };

  return (
    <>
      <div className="w-full bg-white dark:bg-gray-900 shadow-md rounded-lg overflow-hidden border dark:border-gray-700">
        <div className="p-4 flex justify-between items-center border-b dark:border-gray-700">
          <h2 className="text-lg font-semibold dark:text-white">Task Manager</h2>
          <div className="flex space-x-2">
            <button 
              onClick={() => setIsAddingTask(true)}
              className="flex items-center px-3 py-1.5 bg-blue-600 text-white rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
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
              className="flex items-center px-3 py-1.5 bg-green-600 text-white rounded-md hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600"
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
                <th className="p-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Order</th>
                <th className="p-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Target Website</th>
                <th className="p-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Search Keyword</th>
                <th className="p-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                {/* <th className="p-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Loop</th> */}
                <th className="p-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
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
          <div className="p-8 text-center text-gray-500 dark:text-gray-400">
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
      </div>

      {browserAgentResults.length > 0 && (
        <div className="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Results</h2>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {browserAgentResults.map(result => {
              const task = tasks.find(t => t.id === result.taskId)
              return <div key={result.taskId} className="p-4">
                <h3 className="text-md font-medium text-gray-700 dark:text-gray-300 mb-2 space-mono-regular">Task {task.target_website} - "{task.search_keyword}"</h3>
                <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-md overflow-auto max-h-96 text-gray-900 dark:text-gray-100"
                    dangerouslySetInnerHTML={{ __html: result.result }} />
              </div>  
            })}
          </div>
        </div>
      )}
    </>
  );
}

