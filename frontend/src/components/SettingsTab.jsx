import { useState, useEffect } from 'react';

export default function SettingsTab() {
  const [settings, setSettings] = useState({
    processDelay: 0,
    openaiKey: '',
    // proxyData: ''
  });

  useEffect(() => {
    const fetchSettings = async () => {
      const result = await window.pywebview.api.get_settings();
      if(result.status === 'success') {
        setSettings(result.settings);
      }
    };

    fetchSettings();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Implement settings save logic
    console.log('Settings saved:', settings);
    const result = await window.pywebview.api.update_settings(settings);
    console.log('Settings update result:', result);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Settings</h1>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
          <div className="space-y-4">
            {/* Process Delay Input */}
            <div>
              <label htmlFor="processDelay" className="block text-sm font-medium text-gray-700 mb-1">
                Process Delay (seconds)
              </label>
              <input
                type="number"
                id="processDelay"
                name="processDelay"
                value={settings.processDelay}
                onChange={handleChange}
                min="0"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter delay in seconds"
              />
              <p className="text-xs text-gray-500 mt-1 text-right mt-2">
                {settings.processDelay && `${(parseInt(settings.processDelay) / 60).toFixed(2)} minutes`}
              </p>
            </div>

            {/* OpenAI Key Input */}
            <div>
              <label htmlFor="openaiKey" className="block text-sm font-medium text-gray-700 mb-1">
                OpenAI API Key
              </label>
              <input
                type="password"
                id="openaiKey"
                name="openaiKey"
                value={settings.openaiKey}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your OpenAI API key"
              />
            </div>

            
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
          >
            Save Settings
          </button>
        </div>
      </form>
    </div>
  );
}