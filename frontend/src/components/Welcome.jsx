import { useState } from 'react';
import { ArrowRight, Globe, Command, Zap } from 'lucide-react';

/**
 * Welcome Component
 * A modern welcome screen with a sleek design and interactive elements
 */
const Welcome = ({ onGetStarted }) => {
  const [hovering, setHovering] = useState(false);
  
  return (
    <div className="flex flex-col items-center">
      <div className="max-w-4xl w-full bg-white dark:bg-gray-800 rounded-xl border overflow-hidden border-gray-200 dark:border-gray-700">
        <div className="grid md:grid-cols-2">
          {/* Left side - Hero section */}
          <div className="bg-gradient-to-br from-primary-600 to-primary-800 p-10 flex flex-col justify-center">
            <h1 className="text-4xl font-bold text-white mb-6 space-mono-bold">
              Browser Agent
            </h1>
            
            <div className="space-y-4 mb-8">
              <div className="flex items-center text-white">
                <Globe className="mr-3" size={20} />
                <p className="text-white/90">Automate complex web tasks</p>
              </div>
              <div className="flex items-center text-white">
                <Command className="mr-3" size={20} />
                <p className="text-white/90">Natural language instructions</p>
              </div>
              <div className="flex items-center text-white">
                <Zap className="mr-3" size={20} />
                <p className="text-white/90">Save hours of manual work</p>
              </div>
            </div>
          </div>
          
          {/* Right side - Content */}
          <div className="p-10 flex flex-col justify-center">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Welcome
            </h2>
            
            <p className="text-gray-600 dark:text-gray-300 mb-8 text-lg">
              Your intelligent assistant that helps you automate browser tasks with ease.
            </p>
            
            <button
              onClick={onGetStarted}
              onMouseEnter={() => setHovering(true)}
              onMouseLeave={() => setHovering(false)}
              className="inline-flex items-center justify-center px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
            >
              Get Started
              <ArrowRight 
                className={`ml-2 transition-transform duration-300 ${hovering ? 'translate-x-1' : ''}`} 
                size={18}  
              />
            </button>
            
            <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
              Powered by advanced AI technology
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
