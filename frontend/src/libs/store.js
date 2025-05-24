import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

const useStore = create(
  immer((set) => ({
    tasks: [],
    settings: {},
    setTasks: (tasks) => set((state) => {
      state.tasks = tasks;
    }),
    addTask: (task) => set((state) => {
      state.tasks.push(task);
    }),
    removeTask: (taskId) => set((state) => {
      state.tasks = state.tasks.filter((task) => task.id !== taskId);
    }),
    setSettings: (settings) => set((state) => {
      state.settings = settings;
    }),
  }))
);

export default useStore;