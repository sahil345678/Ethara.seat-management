import { ProjectUtilization, FloorUtilization } from '../types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface DashboardChartsProps {
  projectData: ProjectUtilization[];
  floorData: FloorUtilization[];
  summary: any;
}

const COLORS = ['#2563eb', '#10b981', '#8b5cf6'];

export const DashboardCharts = ({ projectData, floorData, summary }: DashboardChartsProps) => {
  const pieData = [
    { name: 'Occupied', value: summary.occupied_seats },
    { name: 'Available', value: summary.available_seats },
    { name: 'Reserved', value: summary.reserved_seats },
  ];

  return (
    <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
      {/* Floor Utilization Chart */}
      <div className="card p-6">
        <h3 className="mb-6 text-lg font-bold text-gray-900 tracking-tight">Floor Utilization</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={floorData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
              <XAxis dataKey="floor" tickFormatter={(val) => `Floor ${val}`} tick={{ fill: '#6b7280', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#6b7280', fontSize: 12 }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ fill: '#f3f4f6' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
              <Bar dataKey="occupied_seats" name="Occupied" fill="#2563eb" radius={[4, 4, 0, 0]} />
              <Bar dataKey="available_seats" name="Available" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Seat Status Distribution Pie Chart */}
      <div className="card p-6">
        <h3 className="mb-6 text-lg font-bold text-gray-900 tracking-tight">Seat Distribution</h3>
        <div className="h-[300px] w-full relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={70} outerRadius={110} paddingAngle={2} dataKey="value" stroke="none">
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            </PieChart>
          </ResponsiveContainer>
          {/* Custom legend */}
          <div className="absolute bottom-0 left-0 w-full flex justify-center space-x-6">
            {pieData.map((entry, idx) => (
              <div key={entry.name} className="flex items-center text-sm font-medium text-gray-600">
                <span className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: COLORS[idx] }}></span>
                {entry.name}
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Project Utilization Horizontal Bar Chart */}
      <div className="card p-6 lg:col-span-2">
        <h3 className="mb-6 text-lg font-bold text-gray-900 tracking-tight">Top Projects by Seat Allocation</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={projectData.slice(0, 8)} layout="vertical" margin={{ top: 10, right: 30, left: 20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e5e7eb" />
              <XAxis type="number" tick={{ fill: '#6b7280', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis dataKey="project_name" type="category" width={140} tick={{ fill: '#4b5563', fontSize: 13, fontWeight: 600 }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ fill: '#f3f4f6' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
              <Bar dataKey="allocated_seats" name="Allocated Seats" fill="#6366f1" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
