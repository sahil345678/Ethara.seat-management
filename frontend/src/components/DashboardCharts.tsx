import { ProjectUtilization, FloorUtilization } from '../types';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface DashboardChartsProps {
  projectData: ProjectUtilization[];
  floorData: FloorUtilization[];
  summary: any;
}

const COLORS = ['#0ea5e9', '#10b981', '#8b5cf6']; // brand-500, emerald-500, violet-500

export const DashboardCharts = ({ projectData, floorData, summary }: DashboardChartsProps) => {
  const pieData = [
    { name: 'Occupied', value: summary.occupied_seats },
    { name: 'Available', value: summary.available_seats },
    { name: 'Reserved', value: summary.reserved_seats },
  ];

  return (
    <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      {/* Floor Utilization Chart */}
      <div className="card p-6">
        <h3 className="mb-6 text-lg font-display font-bold text-surface-900 tracking-tight">Floor Utilization</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={floorData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis dataKey="floor" tickFormatter={(val) => `Floor ${val}`} tick={{ fill: '#64748b', fontSize: 12, fontFamily: 'Inter' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#64748b', fontSize: 12, fontFamily: 'Inter' }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ fill: '#f1f5f9' }} contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)', fontFamily: 'Inter' }} />
              <Bar dataKey="occupied" name="Occupied" fill="#0ea5e9" radius={[6, 6, 0, 0]} />
              <Bar dataKey="available" name="Available" fill="#10b981" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Seat Status Distribution Pie Chart */}
      <div className="card p-6">
        <h3 className="mb-6 text-lg font-display font-bold text-surface-900 tracking-tight">Seat Distribution</h3>
        <div className="h-[300px] w-full relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={80} outerRadius={120} paddingAngle={3} dataKey="value" stroke="none">
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)', fontFamily: 'Inter' }} />
            </PieChart>
          </ResponsiveContainer>
          {/* Custom legend */}
          <div className="absolute bottom-0 left-0 w-full flex justify-center space-x-8">
            {pieData.map((entry, idx) => (
              <div key={entry.name} className="flex items-center text-sm font-medium text-surface-600">
                <span className="w-3.5 h-3.5 rounded-full mr-2.5 shadow-sm" style={{ backgroundColor: COLORS[idx] }}></span>
                {entry.name}
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Project Utilization Horizontal Bar Chart */}
      <div className="card p-6 lg:col-span-2">
        <h3 className="mb-6 text-lg font-display font-bold text-surface-900 tracking-tight">Top Projects by Seat Allocation</h3>
        <div className="h-[320px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={projectData.slice(0, 8)} layout="vertical" margin={{ top: 10, right: 30, left: 20, bottom: 0 }} barSize={24}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
              <XAxis type="number" tick={{ fill: '#64748b', fontSize: 12, fontFamily: 'Inter' }} axisLine={false} tickLine={false} />
              <YAxis dataKey="project_name" type="category" width={160} tick={{ fill: '#334155', fontSize: 13, fontWeight: 500, fontFamily: 'Inter' }} axisLine={false} tickLine={false} />
              <Tooltip cursor={{ fill: '#f1f5f9' }} contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)', fontFamily: 'Inter' }} />
              <Bar dataKey="allocated_seats" name="Allocated Seats" fill="#6366f1" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
