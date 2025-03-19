import { useState } from 'react';
import PropTypes from 'prop-types';
import { ChevronsRight, ChevronsLeft } from 'lucide-react';

/**
 * DashboardTab Component
 * A modern tab component with left-side navigation and right-side content
 * Features:
 * - Toggle between full-width and icon-only navigation
 * - Dark mode support
 * - Customizable icons and content
 * 
 * @example
 * const tabs = [
 *   { id: 'dashboard', label: 'Dashboard', icon: <DashboardIcon />, content: <DashboardContent /> },
 *   { id: 'profile', label: 'Profile', icon: <ProfileIcon />, content: <ProfileContent /> },
 *   { id: 'settings', label: 'Settings', icon: <SettingsIcon />, content: <SettingsContent /> }
 * ];
 * 
 * <DashboardTab 
 *   tabs={tabs}
 *   defaultActiveTab="dashboard"
 *   onTabChange={(tabId) => console.log('Tab changed to:', tabId)}
 * />
 */
const DashboardTab = ({ tabs, defaultActiveTab, onTabChange }) => {
  const [activeTab, setActiveTab] = useState(defaultActiveTab || tabs[0]?.id);
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
    onTabChange?.(tabId);
  };

  return (
    <div className="flex w-full h-full bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
      {/* Left side - Tab headers */}
      <div className={`bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 transition-all duration-300 ${
        isCollapsed ? 'w-20' : 'w-64'
      }`}>
        {/* Toggle button */}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full p-2 flex items-center justify-center border-b border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          {isCollapsed ? (
            <ChevronsRight className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          ) : (
            <ChevronsLeft className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          )}
        </button>

        <div className="p-4">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab.id)}
              className={`w-full flex items-center px-4 py-3 mb-1 rounded-lg transition-all duration-200 group relative ${
                activeTab === tab.id
                  ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              {tab.icon && (
                <span className={`flex-shrink-0 ${isCollapsed ? 'mx-auto' : 'mr-3'}`}>
                  {tab.icon}
                </span>
              )}
              {!isCollapsed && (
                <span className="font-medium">{tab.label}</span>
              )}
              {/* Tooltip for collapsed state */}
              {isCollapsed && (
                <span className="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-sm rounded pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                  {tab.label}
                </span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Right side - Tab content */}
      <div className="flex-1 overflow-auto">
        <div className="p-4">
          {tabs.find(tab => tab.id === activeTab)?.content}
        </div>
      </div>
    </div>
  );
};

DashboardTab.propTypes = {
  tabs: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
      label: PropTypes.string.isRequired,
      icon: PropTypes.element,
      content: PropTypes.element.isRequired,
    })
  ).isRequired,
  defaultActiveTab: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  onTabChange: PropTypes.func,
};

export default DashboardTab;
