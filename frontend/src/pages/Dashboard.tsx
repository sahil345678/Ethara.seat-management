import { useDashboardSummary, useProjectUtilization, useFloorUtilization } from '../hooks/useDashboard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorState } from '../components/ErrorState';
import { DashboardCards } from '../components/DashboardCards';
import { DashboardCharts } from '../components/DashboardCharts';

export const Dashboard = () => {
  // Leverage the Phase 12 Batch 2 hooks to fetch server state in parallel
  const { data: summary, isLoading: isLoadingSummary, isError: isErrorSummary, refetch: refetchSummary } = useDashboardSummary();
  const { data: projectData, isLoading: isLoadingProj, isError: isErrorProj, refetch: refetchProj } = useProjectUtilization();
  const { data: floorData, isLoading: isLoadingFloor, isError: isErrorFloor, refetch: refetchFloor } = useFloorUtilization();

  const isLoading = isLoadingSummary || isLoadingProj || isLoadingFloor;
  const isError = isErrorSummary || isErrorProj || isErrorFloor;
  
  const handleRetry = () => {
    refetchSummary();
    refetchProj();
    refetchFloor();
  };

  if (isLoading) return <LoadingSpinner fullHeight message="Aggregating real-time dashboard metrics..." />;
  if (isError) return <div className="py-12"><ErrorState onRetry={handleRetry} message="Failed to load dashboard telemetry from the server." /></div>;
  
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-display font-bold text-surface-900 tracking-tight">Overview</h1>
        <p className="mt-2 text-base text-surface-500">Real-time metrics for facility occupancy and project mapping.</p>
      </div>
      
      {summary && <DashboardCards summary={summary} />}
      
      {projectData && floorData && summary && (
        <DashboardCharts projectData={projectData} floorData={floorData} summary={summary} />
      )}
    </div>
  );
};
