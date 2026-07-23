type AnalyticsInsightsProps = {
  insights: string[];
};

export function AnalyticsInsights({ insights }: AnalyticsInsightsProps) {
  return (
    <div className="analytics-card rounded-4 p-4 p-lg-5 h-100">
      <p className="text-uppercase small text-secondary fw-semibold mb-1">AI Analytics</p>
      <h3 className="h4 fw-bold mb-4">Insights and signals</h3>
      <div className="d-grid gap-3">
        {insights.map((insight) => (
          <div className="insight-card rounded-4 p-3" key={insight}>
            <p className="mb-0 text-secondary">{insight}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
