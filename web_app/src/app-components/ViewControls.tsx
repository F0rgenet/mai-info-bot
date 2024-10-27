import React from 'react';
import { CalendarDays, CalendarCheck } from 'lucide-react';

type ViewType = 'day' | 'week';
type DayType = 'ПН' | 'ВТ' | 'СР' | 'ЧТ' | 'ПТ' | 'СБ';

interface ViewToggleProps {
  activeView: ViewType;
  onViewChange: (view: ViewType) => void;
}

interface DaySelectorProps {
  activeDay: DayType;
  onDayChange: (day: DayType) => void;
}

export const ViewToggle: React.FC<ViewToggleProps> = ({ activeView, onViewChange }) => {
  return (
    <div className="flex bg-gray-100 rounded-full border-2 border-border">
      <button
        onClick={() => onViewChange('day')}
        className={`flex items-center justify-center flex-1 py-2 px-4 rounded-full transition-all text-sm ${
          activeView === 'day'
            ? 'bg-white shadow-sm text-black'
            : 'text-gray-600 hover:text-gray-800'
        }`}
      >
        <CalendarCheck className="w-4 h-4 mr-2" />
        На день
      </button>
      <button
        onClick={() => onViewChange('week')}
        className={`flex items-center text-sm justify-center flex-1 py-2 px-4 rounded-full transition-all ${
          activeView === 'week'
            ? 'bg-white shadow-sm text-black'
            : 'text-gray-600 hover:text-gray-800'
        }`}
      >
        <CalendarDays className="w-4 h-4 mr-2" />
        На неделю
      </button>
    </div>
  );
};

export const DaySelector: React.FC<DaySelectorProps> = ({ activeDay, onDayChange }) => {
  const days: DayType[] = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'];

  return (
    <div className="flex bg-gray-100 rounded-full border-2 border-border">
      {days.map((day) => (
        <button
          key={day}
          onClick={() => onDayChange(day)}
          className={`flex-1 py-2 px-4 text-sm rounded-full transition-all ${
            activeDay === day
              ? 'bg-white shadow-sm text-black'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          {day}
        </button>
      ))}
    </div>
  );
};

const ViewControls: React.FC = () => {
  const [activeView, setActiveView] = React.useState<ViewType>('day');
  const [activeDay, setActiveDay] = React.useState<DayType>('ПН');

  return (
    <div className="w-full max-w-2xl">
      <ViewToggle activeView={activeView} onViewChange={setActiveView} />
      <div
        className={`transform transition-all duration-600 ease-out origin-top
          ${activeView === 'day' 
            ? 'opacity-100 translate-y-0 h-auto mt-2'
            : 'opacity-0 -translate-y-2 h-0 overflow-hidden mt-0'
          }`}
      >
        <DaySelector activeDay={activeDay} onDayChange={setActiveDay} />
      </div>
    </div>
  );
};

export default ViewControls;